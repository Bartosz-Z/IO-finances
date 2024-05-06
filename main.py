import os.path

import numpy as np
from pymoo.algorithms.moo.age import AGEMOEA
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.sms import SMSEMOA

import constants
from ArgumentParser import ArgumentParser
from loader import Loader
from exchange_model import ExchangeModel
from exchange_rate_problem import ExchangeRateProblem
from json_reader import JSONReader
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.moead import MOEAD
from exchange_rate_data import ExchangeRateData
from data_extractor import DataExtractor
from pymoo.core.callback import Callback
from ExtractorModules.mdd_extractor import MddExtractor
from ExtractorModules.polynomial_extractor import PolynomialExtractor
from ExtractorModules.exponential_extractor import ExponentialExtractor


class ConvergenceCallback(Callback):
    def __init__(self) -> None:
        super().__init__()
        self.n_evals = []
        self.rois = []
        self.mdds = []

    def notify(self, algorithm):
        new_rois = []
        new_mdds = []
        for i in range(algorithm.opt.shape[0]):
            found = False
            roi = -algorithm.opt[i].F[0] * 100
            mdd = algorithm.opt[i].F[1] * 100
            for j in range(len(new_rois)):
                if abs(new_rois[j] - roi) < 0.00001 and abs(new_mdds[j] - mdd) < 0.00001:
                    found = True
                    break
            if not found:
                self.n_evals.append(algorithm.evaluator.n_eval)
                new_rois.append(roi)
                new_mdds.append(mdd)
        self.rois.extend(new_rois)
        self.mdds.extend(new_mdds)


def plot_result(data, genotype, model, ax):
    results = np.empty((1, 2))
    model.evaluate(np.array([genotype]), results, 0, 1)
    roi = results[0][0]
    mdd = results[0][1]
    print(f"Evaluation ROI and MDD: {(-roi * 100):.5f}%, {(mdd * 100):.5f}%")
    print("Genotype:", list(genotype))
    total_money_history = model.get_total_money_history()
    # money_history = model.get_money_history()
    # stocks_history = model.get_stocks_history()
    ax.plot(total_money_history / constants.MONEY_MULTIPLIER)
    # plt.plot(money_history / constants.MONEY_MULTIPLIER)
    # plt.plot(stocks_history * data.history[0] / constants.MONEY_MULTIPLIER)
    ax.plot(data.history / data.history[0] * 1000)
    # plt.legend(['Total money for model', 'Money for model', 'Stocks for model', 'Exchange rate'])


def plot_convergence(callback, verbose=False):
    ax = plt.figure().add_subplot(projection='3d')
    ax.scatter(callback.n_evals, callback.rois, callback.mdds)
    ax.set_xlabel('Number of evaluations')
    ax.set_ylabel('Return of investment')
    ax.set_zlabel('Maximum drawdown')
    plt.show()


def solve(data, algorithm, settings_dict, verbose=False):
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
    problem = ExchangeRateProblem(extractor.get_genotype_size(), model, processes=settings_dict["processes"])
    callback = ConvergenceCallback()
    res = minimize(problem,
                   algorithm,
                   ('n_gen', settings_dict["n_gen"]),
                   callback=callback,
                   seed=settings_dict["seed"],
                   verbose=False)

    unique_inds = []
    for i in range(res.opt.shape[0]):
        found = False
        roi = res.opt[i].F[0]
        mdd = res.opt[i].F[1]
        for j in range(len(unique_inds)):
            if abs(unique_inds[j].F[0] - roi) < 0.00001 and abs(unique_inds[j].F[1] - mdd) < 0.00001:
                found = True
                break
        if not found:
            unique_inds.append(res.opt[i])

    # path_to_population = os.path.join('')
    for i in range(len(unique_inds) // 4):
        fig, axs = plt.subplots(2, 2, sharex='all', sharey='all')
        plot_result(data=data, model=model, genotype=unique_inds[i * 4].X, ax=axs[0, 0])
        plot_result(data=data, model=model, genotype=unique_inds[i * 4 + 1].X, ax=axs[0, 1])
        plot_result(data=data, model=model, genotype=unique_inds[i * 4 + 2].X, ax=axs[1, 0])
        plot_result(data=data, model=model, genotype=unique_inds[i * 4 + 3].X, ax=axs[1, 1])
        fig.legend(['Total money for model', 'Exchange rate'], loc='upper center', ncol=2)
        # plt.savefig('foo.png')
        if verbose:
            plt.show()
    if len(unique_inds) % 4 > 0:
        idx = (len(unique_inds) // 4) * 4
        fig, axs = plt.subplots(2, 2, sharex='all', sharey='all')
        if len(unique_inds) % 4 >= 1:
            plot_result(data=data, model=model, genotype=unique_inds[idx].X, ax=axs[0, 0])
        if len(unique_inds) % 4 >= 2:
            plot_result(data=data, model=model, genotype=unique_inds[idx + 1].X, ax=axs[0, 1])
        if len(unique_inds) % 4 >= 3:
            plot_result(data=data, model=model, genotype=unique_inds[idx + 2].X, ax=axs[1, 0])
        if len(unique_inds) % 4 >= 4:
            plot_result(data=data, model=model, genotype=unique_inds[idx + 3].X, ax=axs[1, 1])
        fig.legend(['Total money for model', 'Exchange rate'], loc='upper center', ncol=2)
        plt.show()
    plt.scatter([-100 * inv.F[0] for inv in unique_inds], [100 * inv.F[1] for inv in unique_inds])
    plt.xlabel("ROI [%]")
    plt.ylabel("MDD [%]")
    plt.show()
    plot_convergence(callback, verbose)


def main():
    argument_parser = ArgumentParser()
    args = argument_parser.parse()
    settings_dict = JSONReader.load(args.json_path)
    loader = Loader()
    data = loader.load_csv_exchange_rate_data(args.data_path)
    data_better = ExchangeRateData(data.history[550:950])
    data_worse = ExchangeRateData(data.history[:400])

    ref_dirs_moead = get_reference_directions("uniform", 2, n_partitions=12)
    moead = MOEAD(
        ref_dirs_moead,
        n_neighbors=200,
        prob_neighbor_mating=0.2,
    )
    nsga2 = NSGA2(pop_size=settings_dict["population_size"])
    ref_dirs_nsga3 = get_reference_directions("das-dennis", 2, n_partitions=12)
    nsga3 = NSGA3(pop_size=settings_dict["population_size"], ref_dirs=ref_dirs_nsga3)
    agemoea = AGEMOEA(pop_size=settings_dict["population_size"])
    smsemoa = SMSEMOA(pop_size=settings_dict["population_size"])

    solve(data=data_worse, algorithm=nsga2, settings_dict=settings_dict, verbose=True)  # Looks good
    # solve(data=data_worse, algorithm=agemoea)
    # solve(data=data_worse, algorithm=moead)
    # solve(data=data_worse, algorithm=nsga3)
    # solve(data=data_worse, algorithm=smsemoa)

    solve(data=data_better, algorithm=nsga2, settings_dict=settings_dict, verbose=True)  # Looks good
    # solve(data=data_better, algorithm=agemoea)
    # solve(data=data_better, algorithm=moead)
    # solve(data=data_better, algorithm=nsga3)
    # solve(data=data_better, algorithm=smsemoa)


if __name__ == '__main__':
    main()
