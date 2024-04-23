from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    def __init__(self, main_extractor):
        self._main_extractor = main_extractor

    @abstractmethod
    def get_parameters_size(self):
        raise NotImplemented
