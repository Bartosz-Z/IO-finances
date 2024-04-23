import numpy as np
import matplotlib.pyplot as plt
from typing import Dict
from base_extractor import BaseExtractor


class PolynomialExtractor(BaseExtractor):
    def __init__(self, main_extractor, polynomial_degree):
        super().__init__(main_extractor)
        self.polynomial_degree = polynomial_degree
        self.__cache: Dict[int, np.ndarray] = {}

    def get_parameters_size(self):
        return self._main_extractor.slice_count * (self.polynomial_degree + 1)

    def _calculate_polynomial_coefficients(self, x, y):
        # Returns: array, the coefficients of the polynomial approximation. Smallest order first.
        A = np.vander(x, self.polynomial_degree + 1)
        coeffs = np.linalg.lstsq(A, y, rcond=None)[0]
        return coeffs[::-1]

    def _polynomial_value(self, x, coeffs):
        deg = len(coeffs)
        val = 0
        for i in range(deg):
            val += x**i * coeffs[i]
        return val

    def _normalize(self, parameters):
        # Get to range [0, inf)
        parameters_min = parameters.min()
        parameters = parameters - parameters_min
        # Apply log
        non_zero_mask = parameters != 0
        parameters[non_zero_mask] = np.log(parameters[non_zero_mask])
        # Get to range [0, 1]
        parameters_max = parameters.max()
        if 0 != parameters_max:
            parameters = parameters / parameters_max
        return parameters

    def get_polynomial_parameters(self, time_step_0):
        if time_step_0 in self.__cache:
            return self.__cache[time_step_0]

        self._main_extractor.check_starting_time_point(time_step_0)
        slice_count = self._main_extractor.slice_count
        slice_overlap = self._main_extractor.slice_overlap
        slice_size = self._main_extractor.slice_size

        parameters = np.zeros((slice_count, self.polynomial_degree + 1))
        slice_shift = slice_size - slice_overlap
        for i in range(slice_count):
            # Calculate last point of slice
            time_step = time_step_0 - i * slice_shift
            data_to_approximate = self._main_extractor.data[time_step-slice_size : time_step]
            X = np.array([i for i in range(slice_size)])
            # Approximate by minimizing MSE of approximation
            parameters[i] = self._calculate_polynomial_coefficients(X, data_to_approximate)

            if self._main_extractor.plot_results:
                print(parameters[i])
                plot_Y = np.array([self._polynomial_value(x, parameters[i]) for x in X])
                plt.plot(X, plot_Y, color="green")
                plt.plot(X, data_to_approximate, color="blue")
                plt.grid()
                plt.show()

        parameters = self._normalize(parameters)
        self.__cache[time_step_0] = parameters
        return parameters
