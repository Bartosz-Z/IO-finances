import matplotlib.pyplot as plt
import numpy as np
import constants
from pymoo.core.callback import Callback
from solution import Solution
from exchange_model import ExchangeModel
from exchange_rate_data import ExchangeRateData
from typing import List, Optional


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


class Evaluator:
    def __init__(self, callback: ConvergenceCallback):
        self._callback: ConvergenceCallback = callback
        self._model: Optional[ExchangeModel] = None
        self._data: Optional[ExchangeRateData] = None
        self._solutions: List[Solution] = []
        self._unique_inds: List[int] = []
        plt.rc('axes', axisbelow=True)

    def set_data(self, data: ExchangeRateData):
        self._data = data

    def set_model(self, model: ExchangeModel):
        self._model = model

    def get_callback(self):
        return self._callback

    def plot_result(self, genotype, ax):
        results = np.empty((1, 2))
        self._model.evaluate(np.array([genotype]), results, 0, 1)
        total_money_history = self._model.get_total_money_history()
        # money_history = model.get_money_history()
        # stocks_history = model.get_stocks_history()
        ax.plot(total_money_history / constants.MONEY_MULTIPLIER)
        # plt.plot(money_history / constants.MONEY_MULTIPLIER)
        # plt.plot(stocks_history * data.history[0] / constants.MONEY_MULTIPLIER)
        ax.plot(self._data.history / self._data.history[0] * 1000)
        # plt.legend(['Total money for model', 'Money for model', 'Stocks for model', 'Exchange rate'])

    def plot_convergence(self):
        ax = plt.figure().add_subplot(projection='3d')
        ax.scatter(self._callback.n_evals, self._callback.rois, self._callback.mdds)
        ax.set_xlabel('Number of evaluations')
        ax.set_ylabel('Return of investment [%]')
        ax.set_zlabel('Maximum drawdown [%]')
        yield 'cov_roi_mdd'

        plt.scatter(self._callback.n_evals, self._callback.rois)
        plt.xlabel("Number of evaluations")
        plt.ylabel("Return of investment [%]")
        yield 'cov_roi'

        plt.scatter(self._callback.n_evals, self._callback.mdds)
        plt.xlabel("Number of evaluations")
        plt.ylabel("Maximum drawdown [%]")
        yield 'cov_mdd'

    def solutions(self):
        for solution in self._solutions:
            yield solution

    def plot_roi_mdd(self, results):
        plt.scatter([-100 * results[inv][0] for inv in self._unique_inds], [100 * results[inv][1] for inv in self._unique_inds])
        plt.xlabel("ROI [%]")
        plt.ylabel("MDD [%]")
        plt.grid(visible=True, alpha=0.5, color='black', linestyle='--', linewidth=1)
        return 'roi_mdd'

    def fit(self, genotypes, results):
        self._unique_inds.clear()
        self._solutions.clear()

        for i in range(genotypes.shape[0]):
            found = False
            roi = results[i][0]
            mdd = results[i][1]
            for j in range(len(self._unique_inds)):
                if abs(results[self._unique_inds[j]][0] - roi) < 0.00001 and abs(
                        results[self._unique_inds[j]][1] - mdd) < 0.00001:
                    found = True
                    break
            if not found:
                self._unique_inds.append(i)

        for i in self._unique_inds:
            self._solutions.append(Solution(-results[i][0] * 100, results[i][1] * 100, genotypes[i]))

    def evaluate(self, genotypes, results):
        self.fit(genotypes, results)

        for i in range(len(self._unique_inds) // 4):
            fig, axs = plt.subplots(2, 2, sharex='all', sharey='all')
            self.plot_result(genotype=genotypes[self._unique_inds[i * 4]], ax=axs[0, 0])
            self.plot_result(genotype=genotypes[self._unique_inds[i * 4 + 1]], ax=axs[0, 1])
            self.plot_result(genotype=genotypes[self._unique_inds[i * 4 + 2]], ax=axs[1, 0])
            self.plot_result(genotype=genotypes[self._unique_inds[i * 4 + 3]], ax=axs[1, 1])
            fig.legend(['Total money for model', 'Exchange rate'], loc='upper center', ncol=2)
            yield i
        if len(self._unique_inds) % 4 > 0:
            idx = (len(self._unique_inds) // 4) * 4
            fig, axs = plt.subplots(2, 2, sharex='all', sharey='all')
            if len(self._unique_inds) % 4 >= 1:
                self.plot_result(genotype=genotypes[self._unique_inds[idx]], ax=axs[0, 0])
            if len(self._unique_inds) % 4 >= 2:
                self.plot_result(genotype=genotypes[self._unique_inds[idx + 1]], ax=axs[0, 1])
            if len(self._unique_inds) % 4 >= 3:
                self.plot_result(genotype=genotypes[self._unique_inds[idx + 2]], ax=axs[1, 0])
            if len(self._unique_inds) % 4 >= 4:
                self.plot_result(genotype=genotypes[self._unique_inds[idx + 3]], ax=axs[1, 1])
            fig.legend(['Total money for model', 'Exchange rate'], loc='upper center', ncol=2)
            yield len(self._unique_inds) // 4
