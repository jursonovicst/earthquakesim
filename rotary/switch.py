import micropython
from machine import Pin


class Switch:

    def __init__(self, pin: Pin):
        self._pin = pin
        self._pin.irq(handler=self._detect, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self._handler = None
        self.last_button_status = self._pin.value()

    def _detect(self, pin: Pin):
        if self.last_button_status == self._pin.value():
            return
        self.last_button_status = self._pin.value()
        if self._pin.value():
            micropython.schedule(self.handler, True)
        else:
            micropython.schedule(self.handler, False)

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler):
        self._handler = handler
