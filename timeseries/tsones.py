from timeseries import TimeSeries


class TSOnes(TimeSeries):

    def __init__(self, samplingrate: float):
        super(TSOnes, self).__init__('ones', 0, samplingrate)

    def _func(self, t) -> float:
        return 1
