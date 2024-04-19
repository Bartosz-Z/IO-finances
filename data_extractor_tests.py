if __name__ == "__main__":
    from loader import Loader
    from data_extrator import DataExtractor

    loader = Loader()
    data = loader.load_csv_exchange_rate_data("Data/franc_swiss_data.csv")
    data.history = data.history[:200]  # TODO To be removed

    DE = DataExtractor(data.history, slice_count=5, slice_size=40, parameters_per_slice=6, slice_overlap=0)
    DE.add_polynomial_module(5)
    DE.add_exponential_module()
    DE.plot_results = True

    # print(DE.get_minimal_time_step())
    # DE.get_exponential_filter_parameters(time_step_0=150, alpha_values=[1, 1, 1, 1, 1])

    # DE.get_polynomial_parameters(150, 5)
    # print(len(DE.wavelet_transform(100).flatten()))
    