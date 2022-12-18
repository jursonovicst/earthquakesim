import time

from machine import Pin, I2C

from rotary import Rotary, Switch
from servo import LinearServo
from sh1106 import SH1106_I2C
from simulator import Earthquake

servo = None
simulator = None
try:
    # init display
    i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
    display = SH1106_I2C(128, 64, i2c, rotate=180)
    display.sleep(False)
    display.print(display.status)

    # init servo
    servo = LinearServo(Pin(28), pmin=500, pmax=2500, range=270, dmin=-5.7, dmax=10.7, armlen=24, freq=100)
    display.print(servo.status)

    servo.distance = servo.dmin
    time.sleep(1)
    servo.distance = servo.dcenter
    time.sleep(1)
    servo.distance = servo.dmax
    time.sleep(1)


    rotary = Rotary(Pin(20, Pin.IN, Pin.PULL_UP), Pin(21, Pin.IN, Pin.PULL_UP))
    switch = Switch(Pin(22, Pin.IN, Pin.PULL_UP))

    simulator = Earthquake(servo, display, rotary, switch)
    display.print(simulator.status)

    simulator.run()
    while True:
        time.sleep(0.1)
except Exception as e:
    display.print(str(e))
finally:
    if simulator is not None:
        simulator.close()
    if servo is not None:
        servo.close()
