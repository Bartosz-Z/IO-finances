import numpy as np
import matplotlib.pyplot as plt

class PolynomialExtractor:
    def __init__(self, main_extractor, polynomial_degree):
        self.main_extractor = main_extractor
        self.polynomial_degree = polynomial_degree

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

    def get_polynomial_parameters(self, time_step_0):
        self.main_extractor.check_starting_time_point(time_step_0)
        slice_count = self.main_extractor.slice_count
        slice_overlap = self.main_extractor.slice_overlap
        slice_size = self.main_extractor.slice_size

        parameters = np.zeros((slice_count, self.polynomial_degree+1))
        slice_shift = slice_size - slice_overlap
        for i in range(slice_count):
            # Calculate last point of slice
            time_step = time_step_0 - i*slice_shift
            data_to_approximate = self.main_extractor.data[time_step-slice_size : time_step]
            X = np.array([i for i in range(slice_size)])
            # Approximate by minimizing MSE of approximation
            parameters[i] = self.calculate_polynomial_coefficients(X, data_to_approximate, self.polynomial_degree)

            if self.main_extractor.plot_results:
                print(parameters[i])
                plot_Y = np.array([self.polynomial_value(x, parameters[i]) for x in X])
                plt.plot(X, plot_Y, color="green")
                plt.plot(X, data_to_approximate, color="blue")
                plt.grid()
                plt.show()

        return parameters