verbose = False
if __name__ == '__main__' and not verbose:
    import matplotlib
    matplotlib.use('Agg')


from ArgumentParser import ArgumentParser
from loader import Loader
from exchange_model import ExchangeModel
from exchange_rate_problem import ExchangeRateProblem
from json_reader import JSONReader
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from data_extractor import DataExtractor
from ExtractorModules.mdd_extractor import MddExtractor
from ExtractorModules.polynomial_extractor import PolynomialExtractor
from ExtractorModules.exponential_extractor import ExponentialExtractor
from output_manager import OutputManager
from evaluator import ConvergenceCallback, Evaluator
from time import time


def solve(data, algorithm, settings_dict, output_manager, evaluator):
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
    problem = ExchangeRateProblem(
        extractor.get_genotype_size(),
        model,
        processes=settings_dict["processes"],
        output_manager=output_manager,
        save_iteration=settings_dict["save_iteration"])
    timer_start = time()
    res = minimize(problem,
                   algorithm,
                   ('n_gen', settings_dict["n_gen"]),
                   callback=evaluator.get_callback(),
                   seed=settings_dict["seed"],
                   verbose=False)
    timer_end = time()
    print(f"Time: {timer_end - timer_start}s")
    output_manager.set_iteration('final')
    output_manager.save_all(res.X, res.F, save_population=True)


def main():
    argument_parser = ArgumentParser()
    args = argument_parser.parse()

    callback = ConvergenceCallback()
    evaluator = Evaluator(callback)
    output_manager = OutputManager(args.exp_name, args.out, evaluator=evaluator, verbose=verbose)
    output_manager.build()

    settings_dict = JSONReader.load(args.json_path)
    loader = Loader()
    data = loader.load_csv_exchange_rate_data(args.data_path)
    nsga2 = NSGA2(pop_size=settings_dict["population_size"])

    solve(data=data, algorithm=nsga2, settings_dict=settings_dict, output_manager=output_manager, evaluator=evaluator)

    # data_better = ExchangeRateData(data.history[550:950])
    # data_worse = ExchangeRateData(data.history[:400])

    # ref_dirs_moead = get_reference_directions("uniform", 2, n_partitions=12)
    # moead = MOEAD(
    #     ref_dirs_moead,
    #     n_neighbors=200,
    #     prob_neighbor_mating=0.2,
    # )

    # ref_dirs_nsga3 = get_reference_directions("das-dennis", 2, n_partitions=12)
    # nsga3 = NSGA3(pop_size=settings_dict["population_size"], ref_dirs=ref_dirs_nsga3)
    # agemoea = AGEMOEA(pop_size=settings_dict["population_size"])
    # smsemoa = SMSEMOA(pop_size=settings_dict["population_size"])

    # solve(data=data_worse, algorithm=nsga2, settings_dict=settings_dict, verbose=True)  # Looks good
    # solve(data=data_worse, algorithm=agemoea)
    # solve(data=data_worse, algorithm=moead)
    # solve(data=data_worse, algorithm=nsga3)
    # solve(data=data_worse, algorithm=smsemoa)

    # solve(data=data_better, algorithm=nsga2, settings_dict=settings_dict, verbose=True)  # Looks good
    # solve(data=data_better, algorithm=agemoea)
    # solve(data=data_better, algorithm=moead)
    # solve(data=data_better, algorithm=nsga3)
    # solve(data=data_better, algorithm=smsemoa)


if __name__ == '__main__':
    main()
