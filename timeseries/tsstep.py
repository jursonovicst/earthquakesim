from math import copysign

from timeseries import TSPeriodic


class TSStep(TSPeriodic):

    def __init__(self, period: float, phase: float, samplingrate: float):
        super(TSStep, self).__init__('step', period, phase, samplingrate)

    #       copysign(1,t)
    #       copysign(1,-t)
    #       copysign(1,-(t-period/2))
    def _func(self, t) -> float:
        return copysign(1, -(t % self._period - self._period / 2))
