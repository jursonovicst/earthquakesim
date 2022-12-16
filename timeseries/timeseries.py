#from abc import abstractmethod


class TimeSeries:

    def __init__(self, name: str, samplingrate: float):
        self._name = name
        self._samplingrate = samplingrate
        self._t = -1 / self._samplingrate

    @property
    def name(self) -> str:
        return self._name

#    @abstractmethod
    def _func(self, t: float) -> float:
        pass

    def __iter__(self):
        self._t = -1 / self._samplingrate
        return self

    def __next__(self) -> float:
        self._t += 1 / self._samplingrate
        return self._func(self._t)
