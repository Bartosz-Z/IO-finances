import numpy as np
import matplotlib.pyplot as plt

def extract_parameters(data, time_step_0, slice_count=5, slice_shift=50, alpha_value = 0.8, slice_size = 100, parameters_per_slice = 6, plot_results = False):

    if plot_results:
        # Plot whole dataset
        plt.plot([i for i in range(len(data))], data)

    def exponential_filter(time_step):
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


    parameters = np.zeros((slice_count, parameters_per_slice))
    for i in range(slice_count):
        # Calculate last point of slice
        time_step = time_step_0 - i*slice_shift
        # Calculate last 6 points of filtered values
        parameters[i] = exponential_filter(time_step)

    if plot_results:
        plt.show()
    return parameters
    
