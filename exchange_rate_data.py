class ExchangeRateData:
    def __init__(self, history):
        self.history = history

    def size(self) -> int:
        return self.history.shape[0]
