# backend/app/assetbot.py

import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Any

class Backtest:
    def __init__(self, symbol: str, initial_money: float = 100000):
        self.symbol = symbol
        self.initial_money = initial_money
        self.fee_rate = 0.001

        self.weight = [0.0]
        self.share = [0.0]
        self.account_value = [initial_money]
        self.position_value = [0.0]
        self.account_balance = [initial_money]

        self.transaction_record = {
            "date": [],
            "order": [],
            "symbol": [],
            "price": [],
            "value": [],
            "fee": [],
            "label": [],
        }

        self._load_data()

    # ----------------------------
    # Data loading
    # ----------------------------
    def _load_data(self) -> None:
    # 1. Download data with auto_adjust=True (modern standard)
    # This makes 'Close' the adjusted price automatically
     raw_history = yf.download(self.symbol, interval="1d", auto_adjust=True)
     raw_acwi = yf.download("ACWI", interval="1d", auto_adjust=True)

    # 2. Flatten MultiIndex columns if they exist
    # This converts ('Close', 'AAPL') -> 'Close'
     if isinstance(raw_history.columns, pd.MultiIndex):
        raw_history.columns = raw_history.columns.get_level_values(0)
     if isinstance(raw_acwi.columns, pd.MultiIndex):
        raw_acwi.columns = raw_acwi.columns.get_level_values(0)

    # 3. Use 'Close' (which is now the adjusted price)
     self.history_data = raw_history["Close"].dropna()
     self.ACWI_data = raw_acwi["Close"].dropna()

     if self.history_data.empty or self.ACWI_data.empty:
        raise ValueError(f"Failed to load data for {self.symbol} or ACWI.")

    # ----------------------------
    # Helper methods
    # ----------------------------
    def _get_last_price(self, date):
        return self.history_data[self.history_data.index <= date].iloc[-1]

    def _get_ma(self, price_series, date, obs_n: int = 100):
        return np.average(price_series[price_series.index < date][-obs_n:])

    # ----------------------------
    # Portfolio update methods
    # ----------------------------
    def _daily_update(self, date):
        self.share.append(self.share[-1])
        self.account_balance.append(self.account_balance[-1])
        self.position_value.append(
            self.share[-1] * self._get_last_price(date)
        )
        self.account_value.append(
            self.account_balance[-1] + self.position_value[-1]
        )
        self.weight.append(
            self.position_value[-1] / self.account_value[-1]
        )

    def _order_update(self, date, weight: float, label: str = ""):
        if weight == round(self.weight[-1], 2):
            self._daily_update(date)
            return

        price = self._get_last_price(date)
        bs = "buy" if weight - self.weight[-1] > 0 else "sell"

        self.transaction_record["date"].append(str(date.date()))
        self.transaction_record["order"].append(bs)
        self.transaction_record["symbol"].append(self.symbol)
        self.transaction_record["price"].append(float(price))

        value_change = self.account_value[-1] * (weight - self.weight[-1])
        fee = abs(value_change * self.fee_rate)

        self.transaction_record["value"].append(float(value_change))
        self.transaction_record["fee"].append(float(fee))
        self.transaction_record["label"].append(label)

        self.weight.append(weight)
        self.position_value.append(weight * self.account_value[-1])
        self.account_value.append(self.account_value[-1] - fee)
        self.account_balance.append(
            self.account_value[-1] - self.position_value[-1]
        )
        self.share.append(self.position_value[-1] / price)

    # ----------------------------
    # Strategy logic
    # ----------------------------
    def backtest_momentum(
        self,
        MA_n1: int = 50,
        MA_n2: int = 200,
        ACWI_MA_obs_n: int = 100,
        start_date: str = "2019-01-01",
        end_date: str = "2019-12-30",
    ):
        date_index = self.history_data.index[
            (self.history_data.index >= start_date)
            & (self.history_data.index < end_date)
        ]

        for i in range(1, len(date_index)):
            d = date_index[i]

            # ACWI rule
            acwi_ma = self._get_ma(self.ACWI_data, d, ACWI_MA_obs_n)
            acwi_price = self.ACWI_data[self.ACWI_data.index < d].iloc[-1]
            acwi_ma_prev = self._get_ma(
                self.ACWI_data, date_index[i - 1], ACWI_MA_obs_n
            )
            acwi_price_prev = self.ACWI_data[
                self.ACWI_data.index < date_index[i - 1]
            ].iloc[-1]

            if acwi_price > acwi_ma and acwi_price_prev < acwi_ma_prev:
                self._order_update(d, 0.99, label="ACWI_UP")
                continue
            elif acwi_price < acwi_ma and acwi_price_prev > acwi_ma_prev:
                self._order_update(d, 0.91, label="ACWI_DOWN")
                continue

            # Symbol MA rule
            ma1 = self._get_ma(self.history_data, d, MA_n1)
            ma2 = self._get_ma(self.history_data, d, MA_n2)
            ma1_prev = self._get_ma(self.history_data, date_index[i - 1], MA_n1)
            ma2_prev = self._get_ma(self.history_data, date_index[i - 1], MA_n2)

            if ma1 > ma2 and ma1_prev < ma2_prev:
                self._order_update(d, 0.99, label="MA_CROSS_UP")
            elif ma1 < ma2 and ma1_prev > ma2_prev:
                self._order_update(d, 0.00, label="MA_CROSS_DOWN")
            else:
                self._daily_update(d)

        self._calculate_performance()

    # ----------------------------
    # Performance
    # ----------------------------
    import numpy as np

    def _calculate_performance(self):
        price_series = pd.Series(self.account_value)
        # Log returns
        returns = (np.log(price_series) - np.log(price_series).shift(1)).dropna() * 252

        # Standard Deviation
        vol = float(returns.std())
        
        # Check if vol is 0 or NaN to avoid division errors
        if np.isnan(vol) or vol == 0:
            self.volatility = 0.0
            self.sharpe = 0.0
        else:
            self.volatility = vol
            # Calculate mean return
            avg_return = float(returns.mean())
            self.sharpe = float((avg_return - 0.02) / self.volatility)

    # FINAL SAFETY CHECK: Replace any remaining NaNs or Infs with 0.0
        if not np.isfinite(self.sharpe):
            self.sharpe = 0.0
        if not np.isfinite(self.volatility):
            self.volatility = 0.0

    # ----------------------------
    # Public API for FastAPI
    # ----------------------------
class Backtest:
    def __init__(self, symbol: str, initial_money: float = 100000):
        self.symbol = symbol
        self.initial_money = float(initial_money)
        self.fee_rate = 0.001

        # State tracking
        self.weight = [0.0]
        self.share = [0.0]
        self.account_value = [self.initial_money]
        self.position_value = [0.0]
        self.account_balance = [self.initial_money]

        self.transaction_record = {
            "date": [],
            "order": [],
            "symbol": [],
            "price": [],
            "value": [],
            "fee": [],
            "label": [],
        }
        
        # Performance metrics
        self.sharpe = 0.0
        self.volatility = 0.0

    def _load_data(self) -> None:
        raw_history = yf.download(self.symbol, period="2y", auto_adjust=True)
        raw_acwi = yf.download("ACWI", period="2y", auto_adjust=True)

        if isinstance(raw_history.columns, pd.MultiIndex):
            raw_history.columns = raw_history.columns.get_level_values(0)
        if isinstance(raw_acwi.columns, pd.MultiIndex):
            raw_acwi.columns = raw_acwi.columns.get_level_values(0)

        self.history_data = raw_history["Close"].dropna()
        self.ACWI_data = raw_acwi["Close"].dropna()

        if self.history_data.empty or self.ACWI_data.empty:
            raise ValueError(f"Failed to load data for {self.symbol} or ACWI.")

    def _get_last_price(self, date):
        return float(self.history_data[self.history_data.index <= date].iloc[-1])

    def _get_ma(self, price_series, date, obs_n: int = 100):
        subset = price_series[price_series.index < date]
        if len(subset) < obs_n:
            return np.nan
        return np.average(subset[-obs_n:])

    def _daily_update(self, date):
        self.share.append(self.share[-1])
        self.account_balance.append(self.account_balance[-1])
        price = self._get_last_price(date)
        self.position_value.append(self.share[-1] * price)
        self.account_value.append(self.account_balance[-1] + self.position_value[-1])
        self.weight.append(self.position_value[-1] / self.account_value[-1])

    def _order_update(self, date, weight: float, label: str = ""):
        price = self._get_last_price(date)
        bs = "buy" if weight - self.weight[-1] > 0 else "sell"

        self.transaction_record["date"].append(str(date.date()))
        self.transaction_record["order"].append(bs)
        self.transaction_record["symbol"].append(self.symbol)
        self.transaction_record["price"].append(float(price))

        value_change = self.account_value[-1] * (weight - self.weight[-1])
        fee = abs(value_change * self.fee_rate)

        self.transaction_record["value"].append(float(value_change))
        self.transaction_record["fee"].append(float(fee))
        self.transaction_record["label"].append(label)

        new_total_val = self.account_value[-1] - fee
        new_pos_val = weight * new_total_val
        
        self.weight.append(weight)
        self.position_value.append(new_pos_val)
        self.account_value.append(new_total_val)
        self.account_balance.append(new_total_val - new_pos_val)
        self.share.append(new_pos_val / price)

    def backtest_momentum(self, MA_n1=50, MA_n2=200, start_date="2024-01-01", end_date="2025-01-01"):
        self._load_data()
        
        date_index = self.history_data.index[
            (self.history_data.index >= start_date) & (self.history_data.index < end_date)
        ]

        for i in range(1, len(date_index)):
            d = date_index[i]
            ma1 = self._get_ma(self.history_data, d, MA_n1)
            ma2 = self._get_ma(self.history_data, d, MA_n2)
            
            # Simple crossover logic
            if ma1 > ma2 and self.weight[-1] < 0.5:
                self._order_update(d, 0.99, label="MA_CROSS_UP")
            elif ma1 < ma2 and self.weight[-1] > 0.5:
                self._order_update(d, 0.00, label="MA_CROSS_DOWN")
            else:
                self._daily_update(d)

        self._calculate_performance()

    def _calculate_performance(self):
        series = pd.Series(self.account_value)
        returns = series.pct_change().dropna()
        vol = float(returns.std() * np.sqrt(252))
        self.volatility = vol if np.isfinite(vol) else 0.0
        
        avg_ret = float(returns.mean() * 252)
        if self.volatility > 0:
            s_ratio = (avg_ret - 0.02) / self.volatility
            self.sharpe = s_ratio if np.isfinite(s_ratio) else 0.0

    def run(self) -> Dict[str, Any]:
        self.backtest_momentum()
        return {
            "symbol": self.symbol,
            "initial_money": float(self.initial_money),
            "sharpe": float(self.sharpe),
            "volatility": float(self.volatility),
            "final_account_value": float(self.account_value[-1]),
            "transactions": self.transaction_record,
        }