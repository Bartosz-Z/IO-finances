class ExchangeRateData:
    def __init__(self, history):
        self.history = history

    def size(self) -> int:
        return self.history.shape[0]

    def __copy__(self):
        return ExchangeRateData(self.history)

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        return ExchangeRateData(self.history.__deepcopy__(memodict))
