
# A demo of LCD/TFT SCREEN DISPLAY with touch screen
# A "penprint" is made to screen wherever the pen is touched to screen

import Image
import ImageDraw
import ImageFont

from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import spidev
from time import sleep

DC = 22
RST = 18
LED = 23
PEN = 24



TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)



# Initialize display.
TFT.initLCD(DC, RST, LED)

TFT.initTOUCH(PEN)

draw = TFT.draw()

TFT.clear((255, 255, 255))
print "Draw on the screen with a pen/stylus"

while 1:
    while not TFT.penDown():
        pass

    pos = TFT.penPosition()
    print pos
    #print ""
    x2=pos[0]
    y2=pos[1]


    TFT.penprint((x2,y2), 2, (0,0,0))


    sleep(.1)
