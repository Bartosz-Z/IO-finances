from abc import ABC, abstractmethod
import numpy as np


class BaseExtractor(ABC):
    def __init__(self, main_extractor):
        self._main_extractor = main_extractor

    @abstractmethod
    def get_parameters_size(self) -> int:
        """Returns size of numpy array returned by 'get_parameters' method"""
        raise NotImplemented

    @abstractmethod
    def get_genotype_data_size(self) -> int:
        """Returns number of fields in genotype which will be read by 'get_parameters' method"""
        raise NotImplemented

    @abstractmethod
    def get_parameters(self, time_step_0: int, genotype: np.ndarray, genotype_data_index: int) -> np.ndarray:
        raise NotImplemented
