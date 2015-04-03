# tft24T    V0.2 April 2015     Brian Lavery    TJCTM24024-SPI    2.4 inch Touch 320x240 SPI LCD

#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so.


import Image
import ImageDraw
import ImageFont

from lib_tft24T import TFT24
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import spidev
from time import sleep

# Raspberry Pi configuration.
DC = 22
RST = 18
CE = 0
LED = 23

# Create TFT LCD display class.


TFT = TFT24(DC, spidev.SpiDev(), CE, GPIO, RST, LED, landscape=False)
# RST may be omitted. Then tie rst pin to +3.3V
# LED may be omitted. Then tie led pin to +3.3V
# If landscape=False or omitted, display defaults to portrait mode
# option (maximum) spi_speed=nnnnn may be added, max speed is 32000000, which is the default

# Initialize display.
TFT.begin()

# Get the PIL Draw object to start drawing on the display buffer.
draw = TFT.draw()

TFT.clear((255, 0, 0))
# Alternatively can clear to a black screen by simply calling:
TFT.clear()


# Draw a blue ellipse.
draw.ellipse((10, 10, 110, 80), outline="green", fill="blue")

# Draw a purple rectangle.
draw.rectangle((10, 90, 110, 160), outline="yellow", fill="purple")


# Draw a white X.
draw.line((10, 170, 110, 230), fill="white")
draw.line((10, 230, 110, 170), fill="white")

# Draw a cyan triangle.  (offscreen if landscape view)
draw.polygon([(10, 275), (110, 240), (110, 310)], outline="black", fill="cyan")
TFT.display()

# Load default font.
#font = ImageFont.load_default()

# Alternatively load a TTF font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('Minecraftia.ttf', 24)

# Write two lines of text on the buffer, one of then rotated.
draw.text((15, 12), 'Hello World!', font=font, fill="White")
draw.textrotated((30, 90), 'A line of text.', 30, font, fill="lightgreen")
TFT.display()   # Let's take a look

TFT.backup_buffer()   # take a snapshot of current display

# wallpaper (320x240 or 240x320) are images that fill the total canvas
TFT.load_wallpaper("yoga.jpg")   # It's a landscape pic. It will align itself to landscape
draw.text((100,100), "YES", font=font, fill=(255,255,0))
TFT.display()     # A completely fresh display
sleep(1)
TFT.load_wallpaper("girl.jpg")    # It's a portrait pic. It will align itself to portrait
TFT.display()

TFT.restore_buffer()     # restore that earlier snapshot view
TFT.display()
sleep(1)

TFT.invert(1)    # test colour inversion mode
sleep(0.5)
TFT.invert(0)
sleep(0.5)
TFT.backlite(0)   # test that backlight LEDs can be controlled
sleep(0.5)
TFT.backlite(1)
sleep(0.5)
TFT.clear()

# Test two methods of adding small images to canvas:
draw.bitmap((32, 0), Image.open('pi_logo.png'), fill="blue") # native 1-bit draw function
draw.pasteimage("rpi3.jpg", (115,0))# custom method for coloured image
draw.pasteimage('bl.jpg', (30,80))
draw.text((135,115), "YES", font=font, fill=(255,0,0))
TFT.display()
sleep(1)

# Now test a long text, auto-wrapped into lines:
TFT.clear()
font=ImageFont.truetype('FreeSans.ttf', 18)
text1 = """Iris's professor father, who had doted on her in her childhood, had insisted she study at
Sydney's Kensington campus, and she had resented that. But Dad's plan did have some perverse logic,
she was finally conceding. She would have done her studies in Canberra, would doubtless have still
lived at home, and would be the same risk-averse mouse she'd always been."""
if TFT.is_landscape:
    draw.textwrapped((0,0), text1, 38, 20, font, "lightblue")
else:
    draw.textwrapped((0,0), text1, 27, 20, font, "lightblue") # a bit narrower for portrait!
TFT.display()
sleep(4)

TFT.clear((90,90,255))
font = ImageFont.truetype('FreeSerifItalic.ttf', 75)
draw.text((15, 35), 'tft24T', font=font, fill="YELLOW")   # signature !

TFT.display()    # that's all f...

#        All colours may be any notation (exc for clear() function):
#        (255,0,0)  =red    (R, G, B) - a tuple
#        0x0000FF   =red    BBGGRR   - note colour order
#        "#FF0000"  =red    RRGGBB   - html style
#        "red"      =red    html colour names, insensitive
