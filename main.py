import numpy as np
from pymoo.algorithms.moo.age import AGEMOEA
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.sms import SMSEMOA

import constants
from loader import Loader
from exchange_model import ExchangeModel
from exchange_rate_problem import ExchangeRateProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.moead import MOEAD
from exchange_rate_data import ExchangeRateData


def plot_result(data, genotype, model, ax):
    eval_res = model.evaluate(np.array([genotype]))[0]
    roi = eval_res[0]
    mdd = eval_res[1]
    print(f"Evaluation ROI and MDD: {(-roi * 100):.5f}%, {(mdd * 100):.5f}%")
    print("Genotype:", genotype)
    total_money_history = model.get_total_money_history()
    # money_history = model.get_money_history()
    # stocks_history = model.get_stocks_history()
    ax.plot(total_money_history / constants.MONEY_MULTIPLIER)
    # plt.plot(money_history / constants.MONEY_MULTIPLIER)
    # plt.plot(stocks_history * data.history[0] / constants.MONEY_MULTIPLIER)
    ax.plot(data.history / data.history[0] * 1000)
    # plt.legend(['Total money for model', 'Money for model', 'Stocks for model', 'Exchange rate'])


def solve(data, algorithm):
    model = ExchangeModel(data)
    problem = ExchangeRateProblem(10, model)
    res = minimize(problem,
                   algorithm,
                   ('n_gen', 1000),
                   seed=106,
                   verbose=False)
    print(res.F)
    print((res.X - 0.5) * 5)
    fig, axs = plt.subplots(2, 2, sharex='all', sharey='all')
    plot_result(data=data, model=model, genotype=res.X[1 * len(res.X) // 4 - 1], ax=axs[0, 0])
    plot_result(data=data, model=model, genotype=res.X[2 * len(res.X) // 4 - 1], ax=axs[0, 1])
    plot_result(data=data, model=model, genotype=res.X[3 * len(res.X) // 4 - 1], ax=axs[1, 0])
    plot_result(data=data, model=model, genotype=res.X[4 * len(res.X) // 4 - 1], ax=axs[1, 1])
    fig.legend(['Total money for model', 'Exchange rate'], loc='upper center', ncol=2)
    plt.show()
    plt.scatter(-100 * res.F[:, 0], 100 * res.F[:, 1])
    plt.xlabel("ROI [%]")
    plt.ylabel("MDD [%]")
    plt.show()


def main():
    loader = Loader()
    data = loader.load_csv_exchange_rate_data("franc_swiss_data.csv")
    print(data.history[:20])
    data_better = ExchangeRateData(data.history[550:950])
    data_worse = ExchangeRateData(data.history[:400])
    print()

    ref_dirs_moead = get_reference_directions("uniform", 2, n_partitions=12)
    moead = MOEAD(
        ref_dirs_moead,
        n_neighbors=200,
        prob_neighbor_mating=0.2,
    )
    nsga2 = NSGA2(pop_size=100)
    ref_dirs_nsga3 = get_reference_directions("das-dennis", 2, n_partitions=12)
    nsga3 = NSGA3(pop_size=100, ref_dirs=ref_dirs_nsga3)
    agemoea = AGEMOEA(pop_size=100)
    smsemoa = SMSEMOA(pop_size=100)

    # solve(data=data_worse, algorithm=nsga2)
    # solve(data=data_worse, algorithm=agemoea)
    solve(data=data_worse, algorithm=moead)  # Looks good
    # solve(data=data_worse, algorithm=nsga3)
    # solve(data=data_worse, algorithm=smsemoa)

    # solve(data=data_better, algorithm=nsga2)
    # solve(data=data_better, algorithm=agemoea)
    solve(data=data_better, algorithm=moead)  # Looks good
    # solve(data=data_better, algorithm=nsga3)
    # solve(data=data_better, algorithm=smsemoa)


if __name__ == '__main__':
    main()
