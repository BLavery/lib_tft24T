
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

TFT.load_wallpaper("calc.png")    # Image of calculator !!!
TFT.display()

# Let's define all "hotspots" on the display. Remember display is showing an image of calculator.
# We examine the image carefully (an image utility on PC?)
# and determine the coordinate points for all corners of the "buttons".
# The array allows us easily to assign a digit or operator to each "button".
hotspots = [
(195,10,222,37, "exit"),    # even the window exit button gets a hotspot !
(18,55,82,83, "1"),
(83,55,151,83, "2"),
(152,55,222,83, "3"),
(18,84,82,113, "4"),
(83,84,151,113, "5"),
(152,84,222,113, "6"),
(18,114,82,141 , "7"),
(83,114,151,141, "8"),
(152,114,222,141 , "9"),
(83,142,152,173 , "0"),
(18,142,82,173 , "--"),
(155,142,222,173, "."),
(18,174,55,202, "+"),
(56,174,95,202, "-"),
(96,174,137,202, "*"),
(138,174,179,202, "/"),
(180,174,222,202, "=") ,
(18,203,222,233, "CLR")]

font = ImageFont.truetype('FreeMonoBold.ttf', 18)

formula=""
while 1:
    # "the calculator"
    while not TFT.penDown():
        pass
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()    # Read corsor position of pen

    spot = TFT.penOnHotspot(hotspots, pos)
    # So what "button" was clicked by the pen?
    if spot == None:
        continue
    if spot == "exit":
        TFT.textdirect((20, 36), "                    ", font, fill="black")
        TFT.textdirect((20, 36), "   --- EXIT ---", font, fill="red")
        TFT.clear((255,0,0))
        exit()
    if spot == "CLR":
        formula = ""
        TFT.textdirect((20, 36), "                    ", font, fill="black")
        sleep(0.6)
        continue
    if spot == "--":
        # negation - leading minus sign
        formula = "-"+formula
        spot=""    # so nothing gets appended to formula
    if spot == "=":
        # Time to evaluate the expression entered. Simply use python maths
        try:
            formula = `eval(formula)`
            formula = "%.15s" % formula    # 15 char limit
            TFT.textdirect((20, 36), "                    ", font, fill="black")
            TFT.textdirect((20, 36), formula+"      ", font, fill="green")
            sleep(0.6)
        except:
            formula = ""
            TFT.textdirect((20, 36), "                    ", font, fill="black")
            TFT.textdirect((20, 36), "Error", font, fill="red")
            sleep(4)
            TFT.textdirect((20, 36), "                    ", font, fill="black")

        continue
    # So im most cases we simply append the one digit or operator character to our formula
    formula += spot  # Add one more char to the formula
    TFT.textdirect((20, 36), formula, font, fill="black")
    # This display method is "direct" ie does not go via the slower canvas method
    sleep(0.3)  # debounce between pen clicks
