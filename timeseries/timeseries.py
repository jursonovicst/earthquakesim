# from abc import abstractmethod


class TimeSeries:

    def __init__(self, name: str, shift: float, samplingrate: float):
        self._name = name

        if samplingrate <= 0:
            raise ValueError(f"Sampling rate ({samplingrate}) must be positive.")
        self._samplingrate = samplingrate

        self.__shift = shift

        self.__t = - 1 / self._samplingrate

    @property
    def name(self) -> str:
        return self._name

    @property
    def samplingrate(self) -> float:
        return self._samplingrate

    @property
    def t(self) -> float:
        return self.__t + self.__shift

    #    @abstractmethod
    def _func(self, t: float) -> float:
        pass

    def __iter__(self):
        self.__t = -1 / self._samplingrate
        return self

    def __next__(self) -> float:
        self.__t += 1 / self._samplingrate
        return self._func(self.t)
