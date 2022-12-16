from math import pi

from timeseries import TimeSeries


class TSPeriodic(TimeSeries):

    def __init__(self, name: str, period: float, samplingrate: float):
        self._period = period
        super(TSPeriodic, self).__init__(name, samplingrate)

    @property
    def phase(self) -> float:
        return 2 * pi * ((self._t / self._period) % 1)

    @phase.setter
    def phase(self, ph):
        # adjust _t to ensure phase
        while not (-0.3 < (phase_delta := ph - self.phase) < 0.3):
            self._t += self._period / 10 * phase_delta / 2 / pi

    @property
    def period(self) -> float:
        return self._period

    @period.setter
    def period(self, v: float):
        if v <= 0:
            raise ValueError(f"Period must be positive, got: {v}")

        # set new period, keep phase
        phase_o = self.phase
        self._period = v
        self.phase = phase_o
