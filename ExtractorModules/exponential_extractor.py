import numpy as np
import matplotlib.pyplot as plt
from ExtractorModules.base_extractor import BaseExtractor


class ExponentialExtractor(BaseExtractor):
    def __init__(self, main_extractor, parameters_per_slice):
        super().__init__(main_extractor)
        self._parameters_per_slice = parameters_per_slice

    def get_parameters_size(self):
        return self._main_extractor.slice_count * self._parameters_per_slice

    def get_genotype_data_size(self) -> int:
        return self._main_extractor.slice_count

    def _exponential_filter(self, time_step, alpha_value):
        slice_size = self._main_extractor.slice_size
        data = self._main_extractor.data

        filtered_data = np.zeros((slice_size,))
        for filtered_index, raw_data_index in enumerate(range(time_step - slice_size, time_step)):
            if filtered_index == 0:
                # Copy first value
                filtered_data[0] = data[time_step - slice_size]
            else:
                # Calculate the rest
                filtered_data[filtered_index] = alpha_value * data[raw_data_index] + (1-alpha_value) * filtered_data[filtered_index-1]
        if self._main_extractor.plot_results:
            # Plot individual filters
            plt.plot([i for i in range(time_step - slice_size, time_step)], filtered_data)
        return self._main_extractor.normalize(filtered_data[-self._parameters_per_slice:])
    
    def get_parameters(self, time_step_0: int, genotype: np.ndarray, genotype_data_index: int) -> np.ndarray:
        data = self._main_extractor.data
        slice_count = self._main_extractor.slice_count
        slice_overlap = self._main_extractor.slice_overlap
        slice_size = self._main_extractor.slice_size

        self._main_extractor.check_starting_time_point(time_step_0)
        if self._main_extractor.plot_results:
            # Plot whole dataset
            plt.plot([i for i in range(len(data))], data)

        parameters = np.zeros((slice_count, self._parameters_per_slice))
        slice_shift = slice_size - slice_overlap
        for i in range(slice_count):
            # Calculate last point of slice
            time_step = time_step_0 - i*slice_shift
            # Calculate last 'parameters_per_slice' points of filtered values
            parameters[i] = self._exponential_filter(time_step, genotype[genotype_data_index + i])

        if self._main_extractor.plot_results:
            plt.show()
        return parameters.ravel()  # Potencjalnie normalize tutaj zamiast w exponential_filter
