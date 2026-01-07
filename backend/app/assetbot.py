# backend/app/assetbot.py

import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, Any
from .models import BacktestRun, MarketPrice
from sqlalchemy.orm import Session

def save_backtest_run(db, result: Dict[str, Any]):
    db.add(
        BacktestRun(
            symbol=result["symbol"],
            sharpe=result["sharpe"],
            volatility=result["volatility"],
            final_value=result["final_account_value"]
        )
    )
    db.commit()


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

        # REVISED CLEANING LOGIC:
        if isinstance(raw_history.columns, pd.MultiIndex):
            # If there's only one ticker, it might still be MultiIndex
            raw_history.columns = raw_history.columns.get_level_values(0)
        if isinstance(raw_acwi.columns, pd.MultiIndex):
            raw_acwi.columns = raw_acwi.columns.get_level_values(0)

        # Ensure we are getting a Series, not a DataFrame with one column
        self.history_data = raw_history["Close"]
        if isinstance(self.history_data, pd.DataFrame):
            self.history_data = self.history_data.iloc[:, 0]
        
        self.ACWI_data = raw_acwi["Close"]
        if isinstance(self.ACWI_data, pd.DataFrame):
            self.ACWI_data = self.ACWI_data.iloc[:, 0]

        self.history_data = self.history_data.dropna()
        self.ACWI_data = self.ACWI_data.dropna()

        if self.history_data.empty:
            raise ValueError(f"No price data found for ticker: {self.symbol}")
        if self.ACWI_data.empty:
            raise ValueError("No price data found for benchmark: ACWI")

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

    def save_prices(db, symbol: str, prices: pd.Series):
        for date, price in prices.items():
            db.add(
                MarketPrice(
                    symbol=symbol,
                    date=date,
                    close_price=float(price)
                )
            )
        db.commit()


    def backtest_momentum(self, MA_n1=21, MA_n2=50, start_date="2025-01-01", end_date="2026-01-01"):
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
    
   