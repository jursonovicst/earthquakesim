from math import acos, radians, cos, pi, degrees

from machine import Pin

from servo import Servo


class LinearServo(Servo):

    def __init__(self, pin: Pin, pmin: int, pmax: int, range: int, dmin:float, dmax:float, armlen: float, freq: int = None):
        if abs(dmin) > armlen or abs(dmax) > armlen:
            raise ValueError(f"Wrong values: {min}, {max}, {armlen}")
        self._dmin = dmin
        self._dmax = dmax
        self._armlen = armlen

        super(LinearServo, self).__init__(pin, pmin, pmax, range, freq)
        print(f"{self.__class__.__name__} initialized with {self._dmin}-{self._dmax}")

    def _distance2degree(self, dist: float) -> float:
        if dist < -self._armlen * cos(pi / 4) or dist > self._armlen * cos(pi / 4):
            raise Exception(f"invalid servo position {dist}, linearity is only in -45°..45°")
        return degrees(acos(dist / self._armlen))

    def _degree2distance(self, degree: float) -> float:
        return self._armlen * cos(radians(degree))

    @property
    def distance(self) -> float:
        return self._degree2distance(self.degree)

    @distance.setter
    def distance(self, v: float):
        self.degree = self._distance2degree(v)

    @property
    def dmin(self) -> float:
        return self._dmin

    @property
    def dmax(self) -> float:
        return self._dmax

    @property
    def dcenter(self) -> float:
        return self.dmin + (self.dmax - self.dmin) / 2
