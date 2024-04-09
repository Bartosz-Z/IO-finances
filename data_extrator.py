import numpy as np
import matplotlib.pyplot as plt

class DataExtractor:

    def __init__(self, data, slice_count, slice_size, parameters_per_slice, slice_overlap):
        self.data = data
        self.slice_count = slice_count
        self.slice_size = slice_size
        self.parameters_per_slice = parameters_per_slice
        self.slice_overlap = slice_overlap
        self.plot_results = False # Debug



    def exponential_filter(self, time_step, alpha_value):
        filtered_data = np.zeros((self.slice_size,))
        for filtered_index, raw_data_index in enumerate(range(time_step - self.slice_size, time_step)):
            if filtered_index == 0:
                # Copy first value
                filtered_data[0] = self.data[time_step - self.slice_size]
            else:
                # Calculate the rest
                filtered_data[filtered_index] = alpha_value * self.data[raw_data_index] + (1-alpha_value) * filtered_data[filtered_index-1]
        if self.plot_results:
            # Plot individual filters
            plt.plot([i for i in range(time_step - self.slice_size, time_step)], filtered_data)
        return filtered_data[-self.parameters_per_slice:]

    def get_minimal_time_step(self):
        slice_shift = self.slice_size - self.slice_overlap
        return (self.slice_count-1) * slice_shift + self.slice_size
    
    def check_starting_time_point(self, time_step):
        # Check if enough data points
        if time_step < self.get_minimal_time_step():
            raise ValueError("Dataset is too small to extract parameters.")
        if time_step > len(self.data) - 1:
            raise ValueError("time_step_0 is too big for given dataset.")


    def get_exponential_filter_parameters(self, time_step_0, alpha_values):
        self.check_starting_time_point(time_step_0)
        if self.plot_results:
            # Plot whole dataset
            plt.plot([i for i in range(len(self.data))], self.data)

        parameters = np.zeros((self.slice_count, self.parameters_per_slice))
        slice_shift = self.slice_size - self.slice_overlap
        for i in range(self.slice_count):
            # Calculate last point of slice
            time_step = time_step_0 - i*slice_shift
            # Calculate last 'parameters_per_slice' points of filtered values
            parameters[i] = self.exponential_filter(time_step, alpha_values[i])

        if self.plot_results:
            plt.show()
        return parameters


    def calculate_polynomial_coefficients(self, x, y, degree):
        # Returns: array, the coefficients of the polynomial approximation. Smallest order first.
        A = np.vander(x, degree + 1)
        coeffs = np.linalg.lstsq(A, y, rcond=None)[0]
        return coeffs[::-1]

    def polynomial_value(self, x, coeffs):
        deg = len(coeffs)
        val = 0
        for i in range(deg):
            val += x**i * coeffs[i]
        return val

    def get_polynomial_parameters(self, time_step_0, degree):
        self.check_starting_time_point(time_step_0)
        parameters = np.zeros((self.slice_count, degree+1))
        slice_shift = self.slice_size - self.slice_overlap
        for i in range(self.slice_count):
            # Calculate last point of slice
            time_step = time_step_0 - i*slice_shift
            data_to_approximate = self.data[time_step-self.slice_size : time_step]
            X = np.array([i for i in range(self.slice_size)])
            # Approximate by minimizing MSE of approximation
            parameters[i] = self.calculate_polynomial_coefficients(X, data_to_approximate, degree)

            if self.plot_results:
                print(parameters[i])
                plot_Y = np.array([self.polynomial_value(x, parameters[i]) for x in X])
                plt.plot(X, plot_Y, color="green")
                plt.plot(X, data_to_approximate, color="blue")
                plt.grid()
                plt.show()

        return parameters
        

