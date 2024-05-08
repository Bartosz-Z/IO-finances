import os
import matplotlib.pyplot as plt
import matplotlib
from typing import Optional
from solution import Solution
from evaluator import Evaluator


class OutputManager:
    def __init__(self,
                 experiment_name: str,
                 output_path: Optional[str],
                 evaluator: Evaluator,
                 verbose: bool = False):
        self._experiment_name = experiment_name
        if output_path is None:
            self._output_path = self._experiment_name
        else:
            self._output_path = os.path.join(output_path, self._experiment_name)
        self._verbose = verbose
        self._solutions: list[Solution] = []
        self._evaluator = evaluator

        self._output_iteration_path: Optional[str] = None
        self._output_population_path: Optional[str] = None
        self._output_solutions_path: Optional[str] = None

    def build(self):
        if os.path.exists(self._output_path):
            raise ValueError(f'Directory [{self._output_path}] already exist')
        os.makedirs(self._output_path)

    def set_iteration(self, iteration):
        if isinstance(iteration, int):
            iteration_id = f'itr_{iteration:05d}'
        else:
            iteration_id = f'itr_{iteration}'
        self._output_iteration_path = os.path.join(self._output_path, iteration_id)
        os.makedirs(self._output_iteration_path)
        self._output_population_path = os.path.join(self._output_iteration_path, 'population')
        os.makedirs(self._output_population_path)
        self._output_solutions_path = os.path.join(self._output_iteration_path, 'solutions.txt')

    def get_evaluator(self):
        return self._evaluator

    def save_all(self, genotypes, results, save_population):
        if save_population:
            for plot_id in self._evaluator.evaluate(genotypes, results):
                self.save_individuals_plot(plot_id)
        else:
            self._evaluator.fit(genotypes, results)
        self.save_solutions()
        for plot_name in self._evaluator.plot_convergence():
            self.save_plot(plot_name)
        self.save_plot(self._evaluator.plot_roi_mdd(results))

    def save_individuals_plot(self, plot_id: int):
        path_to_fig = os.path.join(self._output_population_path, f'indis_{plot_id:03d}.png')
        plt.savefig(path_to_fig)
        if self._verbose:
            plt.show()
        else:
            plt.clf()
            plt.close()

    def save_plot(self, plot_name: str):
        path_to_fig = os.path.join(self._output_iteration_path, f'{plot_name}.png')
        plt.savefig(path_to_fig)
        if self._verbose:
            plt.show()
        else:
            plt.clf()
            plt.close()

    def add_solution(self, solution: Solution):
        self._solutions.append(solution)

    def save_solutions(self):
        with open(self._output_solutions_path, 'w') as solutions_file:
            for solution in self._evaluator.solutions():
                solutions_file.write(f'ROI: {solution.roi}% | MDD: {solution.mdd}%\n'
                                     f'Genotype: {list(solution.genotype)}\n')
