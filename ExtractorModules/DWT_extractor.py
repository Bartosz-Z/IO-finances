from base_extractor import BaseExtractor


class DWTExtractor(BaseExtractor):
    def __init__(self, main_extractor):
        super().__init__(main_extractor)

    def get_parameters_size(self):
        raise NotImplemented
