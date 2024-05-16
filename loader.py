import numpy as np
from exchange_rate_data import ExchangeRateData
import constants


class Loader:
    def __init__(self, encoding='UTF-8'):
        self._encoding = encoding

    def load_csv_exchange_rate_data(self, path: str):
        data = np.genfromtxt(path, delimiter=',', skip_header=1, encoding=self._encoding)
        return ExchangeRateData(np.squeeze((np.flip(data[:, 2:3]) * constants.MONEY_MULTIPLIER).astype(np.int32)))
