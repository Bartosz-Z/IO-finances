import numpy as np
from typing import Dict
from base_extractor import BaseExtractor


class MddExtractor(BaseExtractor):
    def __init__(self, main_extractor):
        super().__init__(main_extractor)
        self.__cache: Dict[int, np.ndarray] = {}

    def get_parameters_size(self):
        return self._main_extractor.slice_count

    def get_maximum_drawdowns(self, time_step_0):
        if time_step_0 in self.__cache:
            return self.__cache[time_step_0]

        mdds = np.zeros(self._main_extractor.slice_count)
        slice_shift = self._main_extractor.slice_size - self._main_extractor.slice_overlap
        for slice_idx in range(self._main_extractor.slice_count):
            time_step = time_step_0 - slice_idx * slice_shift
            slice_data = self._main_extractor.data[time_step - self._main_extractor.slice_size + 1:time_step + 1]
            i = np.argmax(np.maximum.accumulate(slice_data) - slice_data)
            if i == 0:
                j = 0
            else:
                j = np.argmax(slice_data[:i])
            mdds[slice_idx] = (slice_data[j] - slice_data[i]) / slice_data[j]

        self.__cache[time_step_0] = mdds
        return mdds
