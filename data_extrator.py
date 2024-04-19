import numpy as np
import matplotlib.pyplot as plt
import copy
import pywt
from ExtractorModules.polynomial_extractor import PolynomialExtractor
from ExtractorModules.exponential_extractor import ExponentialExtractor

class DataExtractor:

    def __init__(self, data, slice_count, slice_size, parameters_per_slice, slice_overlap):
        self.data = data
        self.slice_count = slice_count
        self.slice_size = slice_size
        self.parameters_per_slice = parameters_per_slice
        self.slice_overlap = slice_overlap
        self.plot_results = False # Debug
        self.polynomial_module = None
        self.exponential_module = None

    def add_polynomial_module(self, polynomial_degree):
        self.polynomial_module = PolynomialExtractor(self, polynomial_degree)

    def add_exponential_module(self):
        self.exponential_module = ExponentialExtractor(self)
    
    def get_parameters(self, time_step_0, alpha_values):
        parameters = []
        if self.polynomial_module:
            parameters.append(self.polynomial_module.get_polynomial_parameters(time_step_0))
        if self.exponential_module:
            parameters.append(self.exponential_module.get_exponential_filter_parameters(time_step_0, alpha_values))
        return np.concatenate(parameters, axis=None)

    def normalize(self, input_data):
        input_data_min = input_data.min()
        input_data_max = input_data.max()
        return (input_data - input_data_min) / (input_data_max - input_data_min)
    
    def get_genotype_size(self):
        exponential_filter_parameters = (self.slice_count + 1) * self.parameters_per_slice
        polynomial_parameters = self.parameters_per_slice
        return exponential_filter_parameters + polynomial_parameters

    def get_minimal_time_step(self):
        slice_shift = self.slice_size - self.slice_overlap
        return (self.slice_count-1) * slice_shift + self.slice_size
    
    def check_starting_time_point(self, time_step):
        # Check if enough data points
        if time_step < self.get_minimal_time_step():
            raise ValueError("Dataset is too small to extract parameters.")
        if time_step > len(self.data) - 1:
            raise ValueError("time_step_0 is too big for given dataset.")    

    def reduce_coeffs(self, coeffs, reduce_num):
        reduced_coeffs = copy.deepcopy(coeffs)
        reduced_coeffs_len = len(reduced_coeffs)

        for i in range(reduced_coeffs_len - reduce_num, reduced_coeffs_len):
            reduced_coeffs[i] = np.zeros_like(reduced_coeffs[i])

        return reduced_coeffs
    
    def wavelet_transform(self, time_step):
        wavelet = 'haar'
        level = 5
        coeffs = pywt.wavedec(self.data[time_step-self.slice_size:time_step], wavelet, level=level)
        # reconstructed_chart = pywt.waverec(coeffs, wavelet)
        coeffs_reduced = self.reduce_coeffs(coeffs, 1)
        reconstructed_chart = pywt.waverec(coeffs_reduced, wavelet)

        if self.plot_results:
            plt.figure(figsize=(10, 5))
            plt.plot(self.data[time_step-self.slice_size:time_step], label='Original Chart')
            plt.plot(reconstructed_chart, label='Reconstructed Signal -1', linestyle='--')
            plt.legend()
            plt.title('Approximation using DWT')
            plt.show()

        coeffs_flattened = []
        for layer in coeffs_reduced:
            coeffs_flattened.extend(layer)
        return np.array(coeffs_flattened)