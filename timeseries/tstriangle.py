from timeseries import TSPeriodic


class TSTriangle(TSPeriodic):

    def __init__(self, period: float, samplingrate: float):
        super(TSTriangle, self).__init__('triangle', period, samplingrate)

    #        t / period * 4
    #        abs(t / period * 4)
    #        abs((t-period/2) / period * 4)
    #        abs((t-period/2) / period * 4)-1
    #        abs((t%period-period/2) / period * 4)-1

    def _func(self, t) -> float:
        return abs((t % self._period - self._period / 2) / self._period * 4) - 1
