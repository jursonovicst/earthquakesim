from math import sqrt, cos, log, pi
from random import random

from timeseries import TimeSeries


class TSRandom(TimeSeries):

    def __init__(self, samplingrate: float):
        super(TSRandom, self).__init__('normal', samplingrate)

    def _func(self, t: float) -> float:
        v = sqrt(-2 * log(random())) * cos(2 * pi * random()) / 3
        if v > 1:
            return 1
        if v < -1:
            return -1
        return v

