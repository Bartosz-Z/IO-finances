import numpy as np
from exchange_rate_data import ExchangeRateData


class Loader:
    def __init__(self, encoding='UTF-8'):
        self._encoding = encoding

    def load_csv_exchange_rate_data(self, path: str):
        data = np.genfromtxt(path, delimiter=',', skip_header=1, encoding=self._encoding)
        return ExchangeRateData(data[:, 2:3].flat)
