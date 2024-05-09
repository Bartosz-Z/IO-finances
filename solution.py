from typing import List


class Solution:
    def __init__(self, roi: float, mdd: float, genotype: List[float]):
        self._roi = roi
        self._mdd = mdd
        self._genotype = genotype

    @property
    def roi(self):
        return self._roi

    @property
    def mdd(self):
        return self._mdd

    @property
    def genotype(self):
        return self._genotype
