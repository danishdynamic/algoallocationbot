# backend/app/assetbot.py

import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List

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
        self.history_data = (
            yf.download(self.symbol, interval="1d")["Adj Close"].dropna()
        )
        self.ACWI_data = (
            yf.download("ACWI", interval="1d")["Adj Close"].dropna()
        )

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
    def _calculate_performance(self):
        price_series = pd.Series(self.account_value)
        returns = (np.log(price_series) - np.log(price_series).shift(1)).dropna() * 252

        self.volatility = float(returns.std())
        self.sharpe = float((returns.mean() - 0.02) / self.volatility)

    # ----------------------------
    # Public API for FastAPI
    # ----------------------------
    def run(self) -> Dict:
        self.backtest_momentum()

        return {
            "symbol": self.symbol,
            "initial_money": self.initial_money,
            "sharpe": self.sharpe,
            "volatility": self.volatility,
            "final_account_value": float(self.account_value[-1]),
            "transactions": self.transaction_record,
        }
