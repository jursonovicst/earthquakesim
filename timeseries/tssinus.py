from math import sin, pi

from timeseries import TSPeriodic


class TSSinus(TSPeriodic):

    def __init__(self, period: float, phase: float, samplingrate: float):
        super(TSSinus, self).__init__('sinus', period, phase, samplingrate)

    def _func(self, t: float) -> float:
        return sin(t * 2 * pi / self.period)
