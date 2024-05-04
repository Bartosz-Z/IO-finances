import ctypes
import numpy as np
from pymoo.core.problem import Problem
from typing import List
from exchange_model import ExchangeModel
from copy import copy
import multiprocessing as mp


class ExchangeRateProblem(Problem):
    def __init__(self, genotype_size: int, model: ExchangeModel, processes: int = 1):
        super().__init__(n_var=genotype_size, n_obj=2, xl=0.0, xu=1.0)
        self._processes_count: int = processes
        self._models: List[ExchangeModel] = [model]
        for _ in range(self._processes_count - 1):
            self._models.append(copy(self._models[0]))

    def _evaluate(self, x, out, *args, **kwargs):
        if self._processes_count > 1:
            shared_out = mp.RawArray(ctypes.c_double, x.shape[0] * self.n_obj)
            out["F"] = np.frombuffer(shared_out).reshape((x.shape[0], self.n_obj))
            shared_genotypes = mp.RawArray(ctypes.c_double, x.size)
            shared_genotypes_np = np.frombuffer(shared_genotypes).reshape(x.shape)
            shared_genotypes_np[:] = x
            per_thread = x.shape[0] // self._processes_count
            last_thread_idx = self._processes_count - 1

            pool = mp.Pool(initializer=ExchangeModel.init_shared_data,
                           initargs=(shared_out, shared_genotypes),
                           processes=self._processes_count)
            for i in range(last_thread_idx):
                pool.apply_async(
                    self._models[i].evaluate_async,
                    args=(x.shape, out["F"].shape, per_thread * i, per_thread * (i + 1)))
            pool.apply_async(
                self._models[last_thread_idx].evaluate_async,
                args=(x.shape, out["F"].shape, per_thread * last_thread_idx, x.shape[0]))
            pool.close()
            pool.join()
        else:
            out["F"] = np.empty((x.shape[0], self.n_obj))
            self._models[0].evaluate(x, out["F"], 0, x.shape[0])
