import numpy as np
import matplotlib.pyplot as plt

class ExponentialExtractor:
    def __init__(self, main_extractor):
        self.main_extractor = main_extractor

    def exponential_filter(self, time_step, alpha_value):
        slice_size = self.main_extractor.slice_size
        data = self.main_extractor.data

        filtered_data = np.zeros((slice_size,))
        for filtered_index, raw_data_index in enumerate(range(time_step - slice_size, time_step)):
            if filtered_index == 0:
                # Copy first value
                filtered_data[0] = data[time_step - slice_size]
            else:
                # Calculate the rest
                filtered_data[filtered_index] = alpha_value * data[raw_data_index] + (1-alpha_value) * filtered_data[filtered_index-1]
        if self.main_extractor.plot_results:
            # Plot individual filters
            plt.plot([i for i in range(time_step - slice_size, time_step)], filtered_data)
        return self.main_extractor.normalize(filtered_data[-self.main_extractor.parameters_per_slice:])
    
    def get_exponential_filter_parameters(self, time_step_0, alpha_values):
        data = self.main_extractor.data
        slice_count = self.main_extractor.slice_count
        slice_overlap = self.main_extractor.slice_overlap
        slice_size = self.main_extractor.slice_size
        parameters_per_slice = self.main_extractor.parameters_per_slice

        self.main_extractor.check_starting_time_point(time_step_0)
        if self.main_extractor.plot_results:
            # Plot whole dataset
            plt.plot([i for i in range(len(data))], data)

        parameters = np.zeros((slice_count, parameters_per_slice))
        slice_shift = slice_size - slice_overlap
        for i in range(slice_count):
            # Calculate last point of slice
            time_step = time_step_0 - i*slice_shift
            # Calculate last 'parameters_per_slice' points of filtered values
            parameters[i] = self.exponential_filter(time_step, alpha_values[i])

        if self.main_extractor.plot_results:
            plt.show()
        return parameters # Potencjalnie normalize tutaj zamiast w exponential_filter