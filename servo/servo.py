from machine import Pin, PWM


class Servo:

    def __init__(self, pin: Pin, pmin: int, pmax: int, range: int, freq: int = None):
        """
        Servo driver.

        :param pin: Signal Pin
        :param pmin: min pulse width (us)
        :param pmax: max pulse width (us)
        :param range: rotation angle (degree)
        :param freq: PWM frequency (Hz), must allow setting the maximal pulse width
        """
        self._pwm = PWM(pin)

        if pmax < pmin:
            raise ValueError("Max " + str(pmax) + "us is smaller than " + str(pmin) + "us min")
        self._pmin = pmin
        self._pmax = pmax
        self._range = range

        # check if frequency is too high
        if freq is not None and freq > self.maxfreq:
            raise ValueError(f"frequency {freq} (period {1 / freq * 1000000:.0f}us) too high")

        self._pwm.freq(int(freq if freq is not None else self.maxfreq))

        print(f"{self.__class__.__name__} initialized with {self._pmin}-{self._pmax}us, freq {self.freq}")

    def close(self):
        self._pwm.deinit()

    def _pulse2degree(self, pulse: int) -> float:
        return (pulse - self._pmin) * self._range / (self._pmax - self._pmin)

    def _degree2pulse(self, degree: float) -> int:
        return int(self._pmin + degree * (self._pmax - self._pmin) / self._range)

    @property
    def pulse(self) -> int:
        """
        Returns pulse width in us
        :return:
        """
        return self._pwm.duty_ns() * 1000

    @pulse.setter
    def pulse(self, v: int):
        if v < self._pmin:
            raise ValueError(v)
        if v > self._pmax:
            raise ValueError(v)
        self._pwm.duty_ns(int(v * 1000))
        # print(f"Setting {self._pulse2degree(v):.1f}° ({v}us) pulse width")

    @property
    def degree(self) -> float:
        return self._pulse2degree(self.pulse)

    @degree.setter
    def degree(self, v: float):
        self.pulse = self._degree2pulse(v)

    @property
    def maxfreq(self) -> int:
        return int(1 / (self._pmax / 1000000 * 1.15))

    @property
    def freq(self) -> int:
        return self._pwm.freq()

    @property
    def status(self) -> str:
        return f"{self.__class__.__name__}: OK"
