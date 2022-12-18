from machine import Timer, Pin

from rotary import Rotary, Switch
from servo import LinearServo
from sh1106 import SH1106
from simulator import Graph
from timeseries import *


class Earthquake:
    MODE_AMP = 0
    MODE_FREQ = 1
    MODE_FUNC = 2
    NUM_MODE = 3

    def __init__(self, servo: LinearServo, display: SH1106, rotary: Rotary, switch: Switch):
        self._servo = servo
        self._display = display
        self._graph = Graph(128, 26 * 2 + 1)
        self._rotary = rotary
        self._rotary.handler = self._rotary_change
        self._switch = switch
        self._switch.handler = self._switch_change
        self._led = Pin("LED", Pin.OUT)

        self._amp = 0
        self._freq = 1
        self._samplingrate = servo.maxfreq / 10
        self._tsclasses = ['TSSinus', 'TSTriangle', 'TSStep', 'TSRandom', 'TSOnes']
        self._ts = eval(self._tsclasses[0])(1 / self._freq, 0, self._samplingrate)

        self._mode = self.MODE_AMP

        self._tim = None
        self._display_tim = Timer(period=100, mode=Timer.PERIODIC, callback=self._refresh_display)

        self._value = 0
        print(f"{self.__class__.__name__} initialized with {self._samplingrate} Hz sampling rate")

    def close(self):
        self.stop()
        self._display_tim.deinit()

    def run(self):
        self._tim = Timer(period=int(1000 / self._samplingrate), mode=Timer.PERIODIC, callback=self._update)
        print(f"Running simulation")

    def stop(self):
        if self._tim is not None:
            self._tim.deinit()
        self._tim = None

    def _update(self, tim: Timer):
        # store value
        assert isinstance(self._ts, TimeSeries), f"Wrong class, got {type(self._ts)}"
        self._value = next(self._ts)
        assert -1 <= self._value <= 1, f"TS must be in -1..1, got {self._value}"

        # set servo position
        self._servo.distance = self._servo.dcenter + self._value * self._amp

        # draw graph
        self._graph.barplot(self._value * self._amp / (self._servo.dmax - self._servo.dmin) * 2)

        # signal
        self._led.toggle()

    @property
    def value(self) -> float:
        return self._value

    # def sinus(self, period: float):
    #     for x in TSSinus(self._amplitude, period).samples(self._samplingrate):
    #         self._servo.setdistance(self._center + x, self._armlen)
    #         self.sleep()
    #
    # def triangle(self, period: float):
    #     for x in TSTriangle(self._amplitude, period).samples(self._samplingrate):
    #         self._servo.setdistance(self._center + x, self._armlen)
    #         self.sleep()

    def center(self):
        self._servo.distance = self._servo.dcenter

    def min(self):
        self._servo.distance = self._servo.dmin

    def max(self):
        self._servo.distance = self._servo.dmax

    def _rotary_change(self, v: int):
        if self._mode == self.MODE_AMP and (
                v < 0 and -(self._servo.dmax - self._servo.dmin) / 2 < self._amp or
                v > 0 and self._amp < (self._servo.dmax - self._servo.dmin) / 2):
            self._amp += v * (self._servo.dmax - self._servo.dmin) / 2 / 20

        elif self._mode == self.MODE_FREQ and (
                v < 0 and 0 < self._freq or v > 0 and self._freq < self._samplingrate / 4):
            self._freq *= 1.1 ** v

            # update period
            if isinstance(self._ts, TSPeriodic):
                self._ts = eval(self._tsclasses[0])(1 / self._freq, self._ts.phase, self._samplingrate)

        elif self._mode == self.MODE_FUNC:
            phase = 0
            if isinstance(self._ts, TSPeriodic):
                phase = self._ts.phase

            if v < 0:
                self._tsclasses.insert(0, self._tsclasses.pop())
            else:
                self._tsclasses.append(self._tsclasses.pop(0))

            if self._tsclasses[0] in ['TSSinus', 'TSTriangle', 'TSStep']:
                self._ts = eval(self._tsclasses[0])(1 / self._freq, phase, self._samplingrate)
            else:
                self._ts = eval(self._tsclasses[0])(self._samplingrate)

    def _switch_change(self, v: bool):
        if v:
            self._mode = (self._mode + 1) % self.NUM_MODE

    def _refresh_display(self, tim: Timer):
        self._display.fill(0)
        assert isinstance(self._ts, TimeSeries), f"Wrong class, got {type(self._ts)}"
        self._display.text(
            f"{'A' if self._mode == self.MODE_AMP else 'a'}{self._amp:.1f} {'F' if self._mode == self.MODE_FREQ else 'f'}{self._freq:.2f} {self._ts.name[:3].upper() if self._mode == self.MODE_FUNC else self._ts.name[:3].lower()}",
            0, 0, 1)
        self._display.blit(self._graph, 0, self._display.height - self._graph.height)
        #        for i in range(0, 128, 8):
        #            self._display.line(i, amp2y(self._amp), i + 4, amp2y(self._amp), 1)
        #            self._display.line(i, amp2y(-self._amp), i + 4, amp2y(-self._amp), 1)

        self._display.show()

    @property
    def status(self) -> str:
        return f"{self.__class__.__name__}: OK"
