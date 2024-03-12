import numpy as np
import math

from exchange_rate_data import ExchangeRateData
import constants


class Model:
    def __init__(self, data: ExchangeRateData, start_money: int = 1000):
        self._data: ExchangeRateData = data
        self._current_step: int = 0
        self._start_step: int = 3
        self._end_step: int = self._data.size()

        self._start_money = start_money * constants.MONEY_MULTIPLIER
        self._current_money: int = self._start_money
        self._current_stocks: int = 0

        self._total_money_history = np.empty(self._end_step, dtype=np.int64)
        self._total_money_history[:self._start_step] = self._current_money
        self._money_history = np.empty(self._end_step, dtype=np.int64)
        self._money_history[:self._start_step] = self._current_money
        self._stocks_history = np.empty(self._end_step, dtype=np.int64)
        self._stocks_history[:self._start_step] = 0

    def reset(self):
        self._current_step: int = 0

        self._current_money: int = self._start_money
        self._current_stocks: int = 0

        self._total_money_history = np.empty(self._end_step, dtype=np.int64)
        self._total_money_history[:self._start_step] = self._current_money
        self._money_history = np.empty(self._end_step, dtype=np.int64)
        self._money_history[:self._start_step] = self._current_money
        self._stocks_history = np.empty(self._end_step, dtype=np.int64)
        self._stocks_history[:self._start_step] = 0

    # Sell or buy stocks
    def _make_decision(self, genotype):
        val = ((genotype[0] - 0.5) * self._data.history[self._current_step - 1] +
               (genotype[1] - 0.5) * self._data.history[self._current_step - 2] +
               (genotype[2] - 0.5) * self._data.history[self._current_step - 3]) * 5
        e_pow = -0.1 * val
        # Check for overflow
        if e_pow > 32:
            val = 0.
        elif e_pow < -32:
            val = 1.
        else:
            val = 1. / (1. + np.exp(e_pow))
        current_rate = self._data.history[self._current_step]

        # For val between 0.45 and 0.55 do nothing
        if val > 0.55:
            # Buy
            max_stocks_to_buy = self._current_money // current_rate
            stocks_to_buy = math.ceil(max_stocks_to_buy * max(1., (val - 0.55) / 0.45))
            self._current_money -= stocks_to_buy * current_rate
            self._current_stocks += stocks_to_buy
        elif val < 0.45:
            # Sell
            stocks_to_sell = math.ceil(self._current_stocks * max(1., (0.45 - val) / 0.45))
            self._current_money += stocks_to_sell * current_rate
            self._current_stocks -= stocks_to_sell

    def _step(self, genotype):
        self._make_decision(genotype)
        self._total_money_history[self._current_step] = self._calculate_total_money()
        self._money_history[self._current_step] = self._current_money
        self._stocks_history[self._current_step] = self._current_stocks

    def evaluate(self, genotypes):
        self.reset()
        result = np.empty((genotypes.shape[0], 2), dtype=np.float64)
        for i, genotype in enumerate(genotypes):
            for s in range(self._start_step, self._end_step):
                self._current_step = s
                self._step(genotype)
            result[i, 0] = -self._calculate_roi()
            result[i, 1] = self._calculate_mdd()
        return result

    def _calculate_total_money(self) -> int:
        return self._current_money + self._current_stocks * self._data.history[self._current_step]

    # TODO: To be removed or moved to unit tests
    def test_mdd(self):
        self.reset()
        self._total_money_history = np.array([
            100, 90, 80, 70, 60, 65, 75, 85, 95, 105, 115, 125, 135, 145, 140, 130, 120, 110, 114, 118, 122, 126, 124,
            121, 99, 89, 79, 69, 59, 49, 39, 48, 58, 68, 88, 128, 158, 208
        ])
        print("mdd: ", self._calculate_mdd())
        print("should be picks: [100, 145, 126, 208]")
        print("should be downs: [60, 110, 39]")
        print("should be mdd: (126 - 39) / 126 = 87 / 126 = 0.69")
        self.reset()
        self._total_money_history = np.array([
            100, 90, 80, 70, 60, 65, 75, 85, 95, 105, 115, 125, 135, 145, 140, 130, 120, 110
        ])
        print("mdd: ", self._calculate_mdd())
        print("should be picks: [100, 145]")
        print("should be downs: [60, 110]")
        print("should be mdd: (100 - 60) / 100 = 40 / 100 = 0.4")
        self.reset()
        self._total_money_history = np.array([
            65, 75, 85, 95, 105, 115, 125, 135, 145, 140, 130, 120, 110, 114, 118, 122, 126, 124,
            121, 99, 89, 79, 69, 59, 49, 39
        ])
        print("mdd: ", self._calculate_mdd())
        print("should be picks: [145, 126]")
        print("should be downs: [110, 39]")
        print("should be mdd: (126 - 39) / 126 = 87 / 126 = 0.69")
        self.reset()

    # Return of investment
    def _calculate_roi(self) -> float:
        return (self._total_money_history[self._end_step - 1] - self._start_money) / self._start_money

    # Maximum drawdown
    def _calculate_mdd(self) -> float:
        picks = []
        downs = []
        last_pick = self._total_money_history[0]
        last_down = self._total_money_history[0]
        if self._total_money_history.shape[0] > 1 and self._total_money_history[1] <= last_pick:
            picks.append(last_pick)

        for money in self._total_money_history:
            if money < last_pick:
                if len(downs) == len(picks):
                    picks.append(last_pick)
                    last_down = money
            else:
                last_pick = money

            if money > last_down:
                if len(downs) < len(picks):
                    downs.append(last_down)
                    last_pick = money
            else:
                last_down = money

        if self._total_money_history.shape[0] > 1:
            if self._total_money_history[-2] > self._total_money_history[-1]:
                downs.append(self._total_money_history[-1])

        mdd = 0.
        for i in range(len(downs)):
            i_mdd = (picks[i] - downs[i]) / picks[i]
            if i_mdd > mdd:
                mdd = i_mdd

        return mdd

    def get_total_money_history(self):
        return np.array(self._total_money_history)

    def get_money_history(self):
        return np.array(self._money_history)

    def get_stocks_history(self):
        return np.array(self._stocks_history)
