
from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import spidev
from time import sleep

# Raspberry Pi configuration.
PEN = 24

TFT = TFT24T(spidev.SpiDev(), GPIO)
# Raw touch output is intrinsically portrait mode

TFT.initTOUCH(PEN)

while 1:
    while not TFT.penDown():
        pass

    print "%03X" % TFT.readValue(TFT.X)
    print "%03X" % TFT.readValue(TFT.Y)

    print ""
    sleep(.5)
