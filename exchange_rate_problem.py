from pymoo.core.problem import Problem
from exchange_model import ExchangeModel


class ExchangeRateProblem(Problem):
    def __init__(self, genotype_size: int, model: ExchangeModel):
        super().__init__(n_var=genotype_size, n_obj=2, xl=0.0, xu=1.0)
        self._model = model

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = self._model.evaluate(x)
