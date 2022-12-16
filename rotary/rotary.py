import micropython
from machine import Pin


class Rotary:

    def __init__(self, dt: Pin, clk: Pin):
        self._dt = dt
        self._clk = clk
        self.last_status = (self._dt.value() << 1) | self._clk.value()
        self._dt.irq(handler=self._rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self._clk.irq(handler=self._rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self._handler = None

    def _rotary_change(self, pin: Pin):
        new_status = (self._dt.value() << 1) | self._clk.value()
        if new_status == self.last_status:
            return
        transition = (self.last_status << 2) | new_status
        if transition == 0b1110:
            micropython.schedule(self.handler, 1)
        elif transition == 0b1101:
            micropython.schedule(self.handler, -1)
        self.last_status = new_status

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler):
        self._handler = handler
