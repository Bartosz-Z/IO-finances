from ExtractorModules.base_extractor import BaseExtractor


class DWTExtractor(BaseExtractor):
    def __init__(self, main_extractor):
        super().__init__(main_extractor)

    def get_parameters_size(self):
        raise NotImplemented

    def get_genotype_data_size(self) -> int:
        raise NotImplemented

    def get_parameters(self, time_step_0: int, genotype: np.ndarray, genotype_data_index: int) -> np.ndarray:
        raise NotImplemented
