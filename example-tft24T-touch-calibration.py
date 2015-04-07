
# A calibration tool - to find parameters of cursor calibration


calib_scale240 = 288   # Likely about 285
calib_scale320 = 391   # Likely about 384
calib_offset240 = 29   # Likely about 28
calib_offset320 = 27   # Likely about 25
# You may amend these 4 values from the output of this procedure

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

print "First pass may show penprint not tracking well on the red lines."
print "Don't worry. Keep the stylus strictly on the red lines. Follow prompts below."
print
sleep(3)

TFT = TFT24T(spidev.SpiDev(), GPIO)

# Initialize display and touch.
TFT.initLCD(DC, RST, LED)
TFT.initTOUCH(PEN)

draw = TFT.draw()

TFT.clear((255, 255, 255))

draw.line((30, 1, 30, 318), fill="red")  # These lines are 30 pixels from each edge
draw.line((1, 30, 238, 30), fill="red")
draw.line((210, 1, 210, 318), fill="red")
draw.line((1, 290, 238, 290), fill="red")
font=ImageFont.truetype('FreeSans.ttf', 26)
draw.text((5, 110), "1", font=font, fill=(255,0,0))
draw.text((225, 110), "2", font=font, fill=(255,0,0))
draw.text((150, 10), "3", font=font, fill=(255,0,0))
draw.text((150, 295), "4", font=font, fill=(255,0,0))
TFT.display()

def avg100(channel):
    count = 0
    v=[]
    while 1:
        while not TFT.penDown():
            pass
        x = TFT.readValue(TFT.X)  # raw 12-bit coordinate from touchscreen device
        y = TFT.readValue(TFT.Y)  # These 2 are for the penprint on display
        # penprint: find lcd coordinates (240x320) according to 4 scaling factors already at top of this file
        x2 = (4096 -x) * calib_scale240 / 4096   -calib_offset240
        y2 = y * calib_scale320 / 4096   - calib_offset320
        TFT.penprint((x2,y2), 2, (0,0,0))

        r = TFT.readValue(channel)  # This is the one we really keep. X or Y
        v += [r]   # accumulate 100 samples
        count += 1
        if count >=100:
            break

        sleep(.01)

    v.sort()  # sort the 100 samples
    v = v[20:85]  # discard extreme values
    av = sum(v)/len(v)  # then take average stylus coordinate (either X or Y)
    return av


print "Run stylus along line 1 until penprints stop ..."
x1= avg100(TFT.X)
print "Line 1 done"
sleep(5)
print "Run stylus along line 2 until penprints stop ..."
x2= avg100(TFT.X)
print "Line 2 done"
sleep(5)
print "Run stylus along line 3 until penprints stop ..."
y1= avg100(TFT.Y)
print "Line 3 done"
sleep(5)
print "Run stylus along line 4 until penprints stop ..."
y2= avg100(TFT.Y)
print "All lines done"
print
print "Calibration complete. These are the 4 magic numbers you need:"

# calc the scaling factors from 4096 system to 240 or 320 system
sc240= 4096*180 / (x1-x2)
sc320= 4096*260 / (y2-y1)

# calc the offset factors
offs240 = (4095-x1)*sc240/4096 - 30
offs320 = y1*sc320/4096 -30

print "Set calib_scale240 to ", sc240
print "Set calib_scale320 to ", sc320
print "Set calib_offset240 to ", offs240
print "Set calib_offset320 to ", offs320
print
print 'These values need to go into top of the file "lib_tft24T.py"'
print "You can also adjust the same 4 at top of THIS file."
print "That should let you repeat this sequence,"
print " confirming the penprints now accurately sit on the red lines"
