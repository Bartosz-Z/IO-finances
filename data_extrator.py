import numpy as np
import matplotlib.pyplot as plt

class DataExtractor:

    def exponential_filter(time_step, data, slice_size, alpha_value, plot_results, parameters_per_slice):
        filtered_data = np.zeros((slice_size,))
        for filtered_index, raw_data_index in enumerate(range(time_step - slice_size, time_step)):
            if filtered_index == 0:
                # Copy first value
                filtered_data[0] = data[time_step - slice_size]
            else:
                # Calculate the rest
                filtered_data[filtered_index] = alpha_value * data[raw_data_index] + (1-alpha_value) * filtered_data[filtered_index-1]
        if plot_results:
            # Plot individual filters
            plt.plot([i for i in range(time_step - slice_size, time_step)], filtered_data)
        return filtered_data[-parameters_per_slice:]


    def exponential_filter_parameters(data, time_step_0, slice_count=5, slice_overlap=50, alpha_value = 0.8, slice_size = 100, parameters_per_slice = 6, plot_results = False):
        # Check if enough data points
        slice_shift = slice_size - slice_overlap
        if time_step_0 - (slice_count-1) * slice_shift - slice_size < 0:
            raise ValueError("Dataset is too small to extract parameters.")
        if time_step_0 > len(data) - 1:
            raise ValueError("time_step_0 is too big for given dataset.")

        if plot_results:
            # Plot whole dataset
            plt.plot([i for i in range(len(data))], data)

        parameters = np.zeros((slice_count, parameters_per_slice))
        for i in range(slice_count):
            # Calculate last point of slice
            time_step = time_step_0 - i*slice_shift
            # Calculate last 'parameters_per_slice' points of filtered values
            parameters[i] = DataExtractor.exponential_filter(time_step, data, slice_size, alpha_value, plot_results, parameters_per_slice)

        if plot_results:
            plt.show()
        return parameters
    
