import numpy as np

import constants
from loader import Loader
from model import Model
from exchange_rate_problem import ExchangeRateProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import matplotlib.pyplot as plt


def main():
    loader = Loader()
    data = loader.load_csv_exchange_rate_data("franc_swiss_data.csv")
    print(data.history[:20])
    data.history = data.history[:200]  # TODO To be removed
    model = Model(data)
    model.test_mdd()
    print()
    problem = ExchangeRateProblem(3, model)
    algorithm = NSGA2(pop_size=100)
    res = minimize(problem,
                   algorithm,
                   ('n_gen', 100),
                   seed=99,
                   verbose=False)
    # print(problem.pareto_front())
    # print(res.F)
    # print(res.X)

    eval_res = model.evaluate(np.array([res.X[0]]))[0]
    roi = eval_res[0]
    mdd = eval_res[1]
    print(f"Evaluation ROI and MDD: {(-roi * 100):.5f}%, {(mdd * 100):.5f}%")
    print("Genotype:", res.X[0])
    total_money_history = model.get_total_money_history()
    # money_history = model.get_money_history()
    # stocks_history = model.get_stocks_history()
    plt.plot(total_money_history / constants.MONEY_MULTIPLIER)
    # plt.plot(money_history / constants.MONEY_MULTIPLIER)
    # plt.plot(stocks_history * data.history[0] / constants.MONEY_MULTIPLIER)
    plt.plot(data.history / data.history[0] * 1000)
    # plt.legend(['Total money for model', 'Money for model', 'Stocks for model', 'Exchange rate'])
    plt.legend(['Total money for model', 'Exchange rate'])
    plt.show()


if __name__ == '__main__':
    main()
