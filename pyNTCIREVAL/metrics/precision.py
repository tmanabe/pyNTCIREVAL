from .metric import Metric

class Precision(Metric):

    def __init__(self, xrelnum, grades, cutoff):
        super(Precision, self).__init__(xrelnum, grades)
        self.cutoff = cutoff

    def gain(self, idx):
        return 1.0 if self._is_relevant(idx) else 0.0

    def discount(self, idx):
        return 1.0 / self.cutoff
