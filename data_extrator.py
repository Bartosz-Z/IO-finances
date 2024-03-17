import numpy as np
import matplotlib.pyplot as plt

class DataExtractor:
    def __init__(self, data):
        self._data = data
        self.filtered_data = np.zeros(data.shape)

        # Time slice settings
        self.time_slices = 5
        self.samples_per_slice = 6
        self.slice_shift = 50

        # Filter settings
        self.alpha_value = 0.5
        self.prepare_filtered_data()

    def prepare_filtered_data(self):
        # Create a set of all filtered date
        self.filtered_data[0] = self._data[0]
        for i in range(1, len(self._data)):
            self.filtered_data[i] = self.alpha_value * self._data[i] + (1-self.alpha_value) * self.filtered_data[i-1]

    def extract_parameters(self):
        # Get parameters from filtered data based on time slice settings
        parameters = np.zeros((self.time_slices, self.samples_per_slice))
        for ts in range(self.time_slices):
            starting_point = ts * self.slice_shift
            parameters[ts, :] = self.filtered_data[starting_point:starting_point+self.samples_per_slice]
        return parameters
    
    def plot_datasets(self):
        plt.plot([i for i in range(len(self._data))], self._data)
        plt.plot([i for i in range(len(self._data))], self.filtered_data)
        plt.grid()
        plt.show()
    
def testExtractor(data):
    DE = DataExtractor(data)
    parameters = DE.extract_parameters()
    print(parameters.shape)

    DE.plot_datasets()

