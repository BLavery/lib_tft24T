# tft24T    V0.2 April 2015     Brian Lavery    TJCTM24024-SPI    2.4 inch Touch 320x240 SPI LCD

#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so.

# A demo of LCD/TFT SCREEN DISPLAY

import Image
import ImageDraw
import ImageFont

from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import spidev
from time import sleep

# Raspberry Pi configuration.
#For LCD TFT SCREEN:
DC = 22
RST = 18
LED = 23

#For PEN TOUCH:
#   (nothing)

# Create TFT LCD/TOUCH object:
TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)
# If landscape=False or omitted, display defaults to portrait mode
# This demo can work in landscape or portrait


# Initialize display.
TFT.initLCD(DC, RST, LED)
# If rst is omitted then tie rst pin to +3.3V
# If led is omitted then tie led pin to +3.3V

# Get the PIL Draw object to start drawing on the display buffer.
draw = TFT.draw()

while 1:
    TFT.clear((255, 0, 0))

    # Alternatively can clear to a black screen by simply calling:
    TFT.clear()


    print "Draw a blue ellipse"
    draw.ellipse((10, 10, 110, 80), outline="green", fill="blue")

    print "Draw a purple rectangle"
    draw.rectangle((10, 90, 110, 160), outline="yellow", fill="purple")


    print "Draw a white X"
    draw.line((10, 170, 110, 230), fill="white")
    draw.line((10, 230, 110, 170), fill="white")

    print "Draw a cyan triangle.  (offscreen if landscape view)"
    draw.polygon([(10, 275), (110, 240), (110, 310)], outline="black", fill="cyan")

    print "Now display it all to screen"
    TFT.display()

    # Load default font.
    #font = ImageFont.load_default()

    # Alternatively load a TTF font.
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    font = ImageFont.truetype('Minecraftia.ttf', 24)

    print "Write two lines of text on the buffer, one of then rotated."
    draw.text((15, 12), 'Hello World!', font=font, fill="White")
    draw.textrotated((30, 90), 'A line of text.', 30, font, fill="lightgreen")
    TFT.display()   # Let's take a look

    print "Save a backup of the canvas"
    TFT.backup_buffer()   # take a snapshot of current display

    # wallpaper (320x240 or 240x320) are images that fill the total canvas
    print "Load a full wallpaper image, a landscape one. It orients automatically."
    print "Write on it, then display all"
    TFT.load_wallpaper("yoga.jpg")   # It's a landscape pic. It will align itself to landscape
    draw.text((100,100), "YES", font=font, fill=(255,255,0))
    TFT.display()     # A completely fresh display
    sleep(1)
    print "Load another image. A portrait one. It automatically adjusts orientation"
    TFT.load_wallpaper("girl.jpg")    # It's a portrait pic. It will align itself to portrait
    TFT.display()

    print "Now restore from that backup. Old display returns."
    TFT.restore_buffer()     # restore that earlier snapshot view
    TFT.display()
    sleep(1)

    print "Test colour-inversion"
    TFT.invert(1)    # test colour inversion mode
    sleep(0.5)
    TFT.invert(0)
    sleep(0.5)
    print "Test the backlight can be turned off"
    TFT.backlite(0)   # test that backlight LEDs can be controlled
    sleep(0.5)
    TFT.backlite(1)
    sleep(0.5)
    TFT.clear()

    # Test two methods of adding small images to canvas:
    print "Paste several images across the canvas, and display"
    draw.bitmap((32, 0), Image.open('pi_logo.png'), fill="blue") # native 1-bit draw function
    draw.pasteimage("rpi3.jpg", (115,0))# custom method for coloured image
    draw.pasteimage('bl.jpg', (30,80))
    draw.text((135,115), "YES", font=font, fill=(255,0,0))
    TFT.display()
    sleep(1)

    print "Test a long para of text, auto-wrapped into screen lines."
    TFT.clear()
    font=ImageFont.truetype('FreeSans.ttf', 18)
    text1 = \
"""Iris's professor father, who had doted on her in her childhood, had insisted she study at
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
    print "show a font in giant letters"
    font = ImageFont.truetype('FreeSerifItalic.ttf', 75)
    draw.text((15, 35), 'tft24T', font=font, fill="YELLOW")   # signature !

    TFT.display()
    sleep(3)
    print "That's all f...    But we will start over ..."
    sleep(2)

#        All colours may be any notation (exc for clear() function):
#        (255,0,0)  =red    (R, G, B) - a tuple
#        0x0000FF   =red    BBGGRR   - note colour order
#        "#FF0000"  =red    RRGGBB   - html style
#        "red"      =red    html colour names, insensitive
