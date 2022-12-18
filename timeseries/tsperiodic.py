from math import pi

from timeseries import TimeSeries


class TSPeriodic(TimeSeries):

    def __init__(self, name: str, period: float, phase: float, samplingrate: float):
        if period <= 0:
            raise ValueError(f"Period ({period}) must be positive")
        self._period = period

        if not 0 <= phase < 2 * pi:
            raise ValueError(f"Phase ({phase:.2f}) must be between 0 and 2π")

        super(TSPeriodic, self).__init__(name, period * phase / 2 / pi, samplingrate)

    @property
    def phase(self) -> float:
        return 2 * pi * ((self.t / self._period) % 1)

    @property
    def period(self) -> float:
        return self._period
