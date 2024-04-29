import numpy as np
import matplotlib.pyplot as plt
import copy
import pywt
from typing import List
from ExtractorModules.base_extractor import BaseExtractor


class DataExtractor:

    def __init__(self, data, slice_count, slice_size, slice_overlap):
        self.data = data
        self.slice_count = slice_count
        self.slice_size = slice_size
        self.slice_overlap = slice_overlap
        self.plot_results = False  # Debug
        self._extractors: List[BaseExtractor] = []

    def add_extractor(self, extractor: BaseExtractor):
        self._extractors.append(extractor)

    def get_weights(self, genotype):
        weights_begin_index = 0
        for extractor in self._extractors:
            weights_begin_index += extractor.get_genotype_data_size()
        return genotype[weights_begin_index:]

    def get_genotype_size(self):
        genotype_size = 0
        for extractor in self._extractors:
            genotype_size += extractor.get_parameters_size() + extractor.get_genotype_data_size()
        return genotype_size

    def get_parameters(self, time_step_0, genotype):
        parameters = []
        current_genotype_data_index = 0
        for extractor in self._extractors:
            parameters.append(extractor.get_parameters(time_step_0, genotype, current_genotype_data_index))
            current_genotype_data_index += extractor.get_genotype_data_size()
        return np.concatenate(parameters, axis=None)

    def normalize(self, input_data):
        input_data_min = input_data.min()
        input_data_max = input_data.max()
        return (input_data - input_data_min) / (input_data_max - input_data_min)

    def get_minimal_time_step(self):
        slice_shift = self.slice_size - self.slice_overlap
        return (self.slice_count - 1) * slice_shift + self.slice_size
    
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