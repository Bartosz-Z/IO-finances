import numpy as np
import math
from copy import deepcopy

from exchange_rate_data import ExchangeRateData
from data_extractor import DataExtractor
import constants


class ExchangeModel:
    def __init__(self, data: ExchangeRateData, data_extractor: DataExtractor, start_money: int = 1000):
        self._data: ExchangeRateData = data
        self._data_extractor = data_extractor
        self._provision: float = 0.001

        self._current_step: int = 0
        self._start_step: int = self._data_extractor.get_minimal_time_step()
        self._end_step: int = self._data.size()

        self._start_money: int = start_money * constants.MONEY_MULTIPLIER
        self._current_money: int = self._start_money
        self._current_stocks: int = 0

        self._total_money_history = np.empty(self._end_step, dtype=np.int64)
        self._total_money_history[:self._start_step] = self._current_money
        self._money_history = np.empty(self._end_step, dtype=np.int64)
        self._money_history[:self._start_step] = self._current_money
        self._stocks_history = np.empty(self._end_step, dtype=np.int64)
        self._stocks_history[:self._start_step] = 0

        self._ln_99 = np.log(99.)

    def __copy__(self):
        cls = self.__class__
        model = cls.__new__(cls)

        model._data = self._data
        model._data_extractor = self._data_extractor
        model._provision = self._provision
        model._current_step = self._current_step
        model._start_step = self._start_step
        model._end_step = self._end_step
        model._start_money = self._start_money
        model._current_money = self._current_money
        model._current_stocks = self._current_stocks
        model._ln_99 = self._ln_99

        model._total_money_history = deepcopy(self._total_money_history)
        model._money_history = deepcopy(self._money_history)
        model._stocks_history = deepcopy(self._stocks_history)

        return model

    def reset(self):
        self._current_step = 0

        self._current_money = self._start_money
        self._current_stocks = 0

        self._total_money_history = np.empty(self._end_step, dtype=np.int64)
        self._total_money_history[:self._start_step] = self._current_money
        self._money_history = np.empty(self._end_step, dtype=np.int64)
        self._money_history[:self._start_step] = self._current_money
        self._stocks_history = np.empty(self._end_step, dtype=np.int64)
        self._stocks_history[:self._start_step] = 0

    # Sell or buy stocks
    def _make_decision(self, genotype):
        parameters = self._data_extractor.get_parameters(self._current_step, genotype)
        val = np.dot(self._data_extractor.get_weights(genotype) - 0.5, parameters.flat) * 20
        e_pow = -self._ln_99 * val / parameters.size
        # Check for overflow
        if e_pow > 16:
            val = 0.
        elif e_pow < -16:
            val = 1.
        else:
            val = 1. / (1. + np.exp(e_pow))
        current_rate = self._data.history[self._current_step]

        up_current_rate = int(round((1. + self._provision) * current_rate))
        down_current_rate = int(round((1. - self._provision) * current_rate))

        # For val between 0.49 and 0.51 do nothing
        if val > 0.51:
            # Buy
            max_stocks_to_buy = self._current_money // up_current_rate
            stocks_to_buy = math.ceil(max_stocks_to_buy * max(1., (val - 0.51) / 0.49))
            self._current_money -= stocks_to_buy * up_current_rate
            self._current_stocks += stocks_to_buy
        elif val < 0.49:
            # Sell
            stocks_to_sell = math.ceil(self._current_stocks * max(1., (0.49 - val) / 0.49))
            self._current_money += stocks_to_sell * down_current_rate
            self._current_stocks -= stocks_to_sell

    def _step(self, genotype):
        self._make_decision(genotype)
        self._total_money_history[self._current_step] = self._calculate_total_money()
        self._money_history[self._current_step] = self._current_money
        self._stocks_history[self._current_step] = self._current_stocks

    @classmethod
    def init_shared_data(cls, shared_out_, shared_genotypes_):
        global shared_out, shared_genotypes
        shared_out = shared_out_
        shared_genotypes = shared_genotypes_

    def evaluate_async(self, genotypes_shape, out_shape, begin_index, end_index, investment_time: int = 0):
        genotypes = np.frombuffer(shared_genotypes).reshape(genotypes_shape)
        out = np.frombuffer(shared_out).reshape(out_shape)
        for i in range(begin_index, end_index):
            self.reset()
            for s in range(self._start_step, max(self._start_step, self._end_step - investment_time)):
                self._current_step = s
                self._step(genotypes[i])
            out[i, 0] = -self._calculate_roi()
            out[i, 1] = self._calculate_mdd()

    def evaluate(self, genotypes, out, begin_index, end_index, investment_time: int = 0):
        for i in range(begin_index, end_index):
            self.reset()
            for s in range(self._start_step, max(self._start_step, self._end_step - investment_time)):
                self._current_step = s
                self._step(genotypes[i])
            out[i, 0] = -self._calculate_roi()
            out[i, 1] = self._calculate_mdd()

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
        print("should be mdd: (145 - 39) / 126 = 106 / 145 = 0.73")
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
        print("should be mdd: (145 - 39) / 126 = 106 / 145 = 0.73")
        self.reset()

    # Return of investment
    def _calculate_roi(self) -> float:
        return (self._total_money_history[self._end_step - 1] - self._start_money) / self._start_money

    # Maximum drawdown
    def _calculate_mdd(self) -> float:
        i = np.argmax(np.maximum.accumulate(self._total_money_history) - self._total_money_history)
        if i == 0:
            j = 0
        else:
            j = np.argmax(self._total_money_history[:i])
        return (self._total_money_history[j] - self._total_money_history[i]) / self._total_money_history[j]

    def get_total_money_history(self):
        return np.array(self._total_money_history)

    def get_money_history(self):
        return np.array(self._money_history)

    def get_stocks_history(self):
        return np.array(self._stocks_history)
