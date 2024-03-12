import numpy as np
from loader import Loader


def main():
    loader = Loader()
    data = loader.load_csv_exchange_rate_data("franc_swiss_data.csv")
    print(data.history[:20])


if __name__ == '__main__':
    main()
