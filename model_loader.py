from ArgumentParserModelLoader import ArgumentParser
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

def plot_result(model, genotype, ax, data):
    results = np.empty((1, 2))
    model.evaluate(np.array([genotype]), results, 0, 1)
    roi = -results[0][0] * 100
    mdd = results[0][1] * 100
    total_money_history = model.get_total_money_history()
    ax.plot(total_money_history / constants.MONEY_MULTIPLIER)
    ax.plot(data.history / data.history[0] * 1000)
    print("ROI: " + str(roi) + "%")
    print("MDD: " + str(mdd) + "%")

def main():
    argument_parser = ArgumentParser()
    args = argument_parser.parse()
    settings_dict = JSONReader.load(args.json_path)
    
    with open(args.genotype_path, "r") as f:
        genotype = eval(f.readline())
        genotype = np.array(genotype)

    loader = Loader()
    data = loader.load_csv_exchange_rate_data(args.data_path)

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


    fig, axs = plt.subplots(1, 1) 
    plot_result(model, genotype, axs, data)
    plt.show()

    # python model_loader.py expo setup.json -data_path="data/franc_swiss_data.csv" -genotype_path="genotype.txt"

if __name__ == "__main__":
    main()