from math import sin, pi

from timeseries import TSPeriodic


class TSSinus(TSPeriodic):

    def __init__(self, period: float, samplingrate: float):
        super(TSSinus, self).__init__('sinus', period, samplingrate)

    def _func(self, t) -> float:
        return sin(t / self._period * 2 * pi)
