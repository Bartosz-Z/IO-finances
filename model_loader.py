from ArgumentParser import ArgumentParser
from json_reader import JSONReader
from exchange_model import ExchangeModel
from loader import Loader
from data_extractor import DataExtractor
from ExtractorModules.mdd_extractor import MddExtractor
from ExtractorModules.polynomial_extractor import PolynomialExtractor
from ExtractorModules.exponential_extractor import ExponentialExtractor
import numpy as np
import matplotlib.pyplot as plt
import constants
from evaluator import Evaluator, ConvergenceCallback


def main():
    argument_parser = ArgumentParser()
    args = argument_parser.parse()
    settings_dict = JSONReader.load(args.json_path)
    if args.genotype_path:
        f = open(args.genotype_path, "r")
        genotype = eval(f.readline())
        f.close()

        loader = Loader()
        data = loader.load_csv_exchange_rate_data(args.data_path)
        callback = ConvergenceCallback()
        evaluator = Evaluator(callback)

        extractor = DataExtractor(data.history,
                            settings_dict["slice_count"],
                            settings_dict["slice_size"],
                            settings_dict["slice_overlap"])
        if settings_dict["use_polynomial_extractor"]:
            extractor.add_extractor(PolynomialExtractor(main_extractor=extractor, polynomial_degree=settings_dict["polynomial_degree"]))
        if settings_dict["use_exponential_extractor"]:
            extractor.add_extractor(ExponentialExtractor(main_extractor=extractor, parameters_per_slice=settings_dict["exp_parameters_per_slice"]))
        if settings_dict["use_mdd_extractor"]:
            extractor.add_extractor(MddExtractor(main_extractor=extractor))

        model = ExchangeModel(data, extractor, settings_dict["start_money"])
        evaluator.set_data(data)
        evaluator.set_model(model)

        genotype = np.array(genotype)

        fig, axs = plt.subplots(1, 1) 
        evaluator.plot_result(genotype, axs, show_roi_and_mdd=True)
        plt.show()

        # python model_loader.py expo setup.json -data_path="data/franc_swiss_data.csv" -genotype_path="genotype.txt"

if __name__ == "__main__":
    main()