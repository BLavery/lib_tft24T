# tft24T    V0.2 April 2015     Brian Lavery    TJCTM24024-SPI    2.4 inch Touch 320x240 SPI LCD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so.


import numbers
import time

import Image
import ImageDraw
import textwrap

from types import MethodType

# Constants for interacting with display registers.
ILI9341_TFTWIDTH    = 240
ILI9341_TFTHEIGHT   = 320

ILI9341_SWRESET     = 0x01
ILI9341_SLPOUT      = 0x11
ILI9341_INVOFF      = 0x20
ILI9341_INVON       = 0x21
ILI9341_GAMMASET    = 0x26
ILI9341_DISPON      = 0x29
ILI9341_CASET       = 0x2A
ILI9341_PASET       = 0x2B
ILI9341_RAMWR       = 0x2C
ILI9341_RAMRD       = 0x2E
ILI9341_MADCTL      = 0x36
ILI9341_PIXFMT      = 0x3A
ILI9341_FRMCTR1     = 0xB1
ILI9341_DFUNCTR     = 0xB6

ILI9341_PWCTR1      = 0xC0
ILI9341_PWCTR2      = 0xC1
ILI9341_VMCTR1      = 0xC5
ILI9341_VMCTR2      = 0xC7
ILI9341_GMCTRP1     = 0xE0
ILI9341_GMCTRN1     = 0xE1


Buffer = None
# textrotated custom method for our "draw" cannot find TFT's canvas buffer if it is not global.
# This method obviously precludes multiple instances of TFT running independently!

class TFT24():
    """Representation of an ILI9341 TFT LCD."""

    def __init__(self, dc, spi, ce, gpio, rst=None, led=None, landscape=False, spi_speed=None):
        global Buffer

        self.is_landscape = landscape
        self._dc = dc
        self._rst = rst
        self._led = led
        self._spi = spi
        self._spi.open(0, ce)    # CE is 0 or 1   (means pin CE0 or CE1)
        if spi_speed == None:
            self._spi.max_speed_hz=32000000
        else:
            self._spi.max_speed_hz=spi_speed
        self._gpio = gpio
        # Set DC as output.
        gpio.setup(dc, gpio.OUT)
        # Setup reset as output (if provided).
        if rst is not None:
            gpio.setup(rst, gpio.OUT)
        if led is not None:
            gpio.setup(led, gpio.OUT)
            gpio.output(led, gpio.HIGH)

        # Create an image buffer.
        if landscape:
            Buffer = Image.new('RGB', (ILI9341_TFTHEIGHT, ILI9341_TFTWIDTH))
        else:
            Buffer = Image.new('RGB', (ILI9341_TFTWIDTH, ILI9341_TFTHEIGHT))
        self.buffer2 = Buffer.copy()

    def send(self, data, is_data=True, chunk_size=4096):
        """Write a byte or array of bytes to the display. Is_data parameter
        controls if byte should be interpreted as display data (True) or command
        data (False).  Chunk_size is an optional size of bytes to write in a
        single SPI transaction, with a default of 4096.
        """
        # Set DC low for command, high for data.
        self._gpio.output(self._dc, is_data)
        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]
        # Write data a chunk at a time.
        for start in range(0, len(data), chunk_size):
            end = min(start+chunk_size, len(data))
            self._spi.writebytes(data[start:end])

    def command(self, data):
        """Write a byte or array of bytes to the display as command data."""
        self.send(data, False)

    def data(self, data):
        """Write a byte or array of bytes to the display as display data."""
        self.send(data, True)

    def reset(self):
        """Reset the display, if reset pin is connected."""
        if self._rst is not None:
            self._gpio.output(self._rst, self._gpio.HIGH)
            time.sleep(0.005)
            self._gpio.output(self._rst, self._gpio.LOW)
            time.sleep(0.02)
            self._gpio.output(self._rst, self._gpio.HIGH)
            time.sleep(0.150)
        else:
            self.command(ILI9341_SWRESET)
            sleep(1)

    def _init(self):
        self.command(ILI9341_PWCTR1)
        self.data(0x23)
        self.command(ILI9341_PWCTR2)
        self.data(0x10)
        self.command(ILI9341_VMCTR1)
        self.data([0x3e, 0x28])
        self.command(ILI9341_VMCTR2)
        self.data(0x86)
        self.command(ILI9341_MADCTL)
        self.data(0x48)
        self.command(ILI9341_PIXFMT)
        self.data(0x55)
        self.command(ILI9341_FRMCTR1)
        self.data([0x00, 0x18])
        self.command(ILI9341_DFUNCTR)
        self.data([0x08, 0x82, 0x27])
        self.command(0xF2)
        self.data(0x00)
        self.command(ILI9341_GAMMASET)
        self.data(0x01)
        self.command(ILI9341_GMCTRP1)
        self.data([0x0F, 0x31, 0x2b, 0x0c, 0x0e, 0x08, 0x4e, 0xf1, 0x37, 0x07, 0x10, 0x03, 0x0e, 0x09, 0x00])
        self.command(ILI9341_GMCTRN1)
        self.data([0x00, 0x0e, 0x14, 0x03, 0x11, 0x07, 0x31, 0xc1, 0x48, 0x08, 0x0f, 0x0c, 0x31, 0x36, 0x0f])
        self.command(ILI9341_SLPOUT)
        time.sleep(0.120)
        self.command(ILI9341_DISPON)

    def begin(self):
        self.reset()
        self._init()

    def set_frame(self, x0=0, y0=0, x1=None, y1=None):
        """Set the pixel address window for proceeding drawing commands. x0 and
        x1 should define the minimum and maximum x pixel bounds.  y0 and y1
        should define the minimum and maximum y pixel bound.  If no parameters
        are specified the default will be to update the entire display from 0,0
        to 239,319.
        """
        # IN THIS LIBRARY, ONLY FULL SCREEN IS ADDRESSED !

        if x1 is None:
            x1 = ILI9341_TFTWIDTH-1
        if y1 is None:
            y1 = ILI9341_TFTHEIGHT-1
        self.command(ILI9341_CASET)        # Column addr
        self.data([x0 >> 8, x0, x1 >> 8, x1])
        self.command(ILI9341_PASET)        # Row addr
        self.data([y0 >> 8, y0, y1 >> 8, y1])
        self.command(ILI9341_RAMWR)

    def display(self, image=None):
        """Write the display buffer or provided image to the hardware.  If no
        image parameter is provided the display buffer will be written to the
        hardware.  If an image is provided, it should be RGB format and the
        same dimensions as the display hardware.
        """
        # By default write the internal buffer to the display.
        if image is None:
            image = Buffer
        if image.size[0] == 320:
            image = image.rotate(90)

        # Set address bounds to entire display.
        self.set_frame()
        # Convert image to array of 16bit 565 RGB data bytes.
        pixelbytes = list(self.image_to_data(image))
        # Write data to hardware.
        self.data(pixelbytes)

    def clear(self, color=(0,0,0)):
        """
        Clear the image buffer to the specified RGB color (default black).
        USE (r, g, b) NOTATION FOR THE COLOUR !!
        """

        if type(color) != type((0,0,0)):
            print "clear() function colours must be in (255,255,0) form"
            exit()
        width, height = Buffer.size
        Buffer.putdata([color]*(width*height))
        self.display()

    def draw(self):
        """Return a PIL ImageDraw instance for 2D drawing on the image buffer."""
        d = ImageDraw.Draw(Buffer)
        # Add custom methods to the draw object:
        d.textrotated = MethodType(_textrotated, d, ImageDraw.Draw)
        d.pasteimage = MethodType(_pasteimage, d, ImageDraw.Draw)
        d.textwrapped = MethodType(_textwrapped, d, ImageDraw.Draw)
        return d

    def load_wallpaper(self, filename):
        # The image should be 320x240 or 240x320 only (full wallpaper!). Errors otherwise.
        # We need to cope with whatever orientations file image and TFT canvas are.
        image = Image.open(filename)
        if image.size[0] > Buffer.size[0]:
            Buffer.paste(image.rotate(90))
        elif image.size[0] < Buffer.size[0]:
            Buffer.paste(image.rotate(-90))
        else:
            Buffer.paste(image)

    def backup_buffer(self):
        self.buffer2.paste(Buffer)

    def restore_buffer(self):
        Buffer.paste(self.buffer2)

    def invert(self, onoff):
        if onoff:
            self.command(ILI9341_INVON)
        else:
            self.command(ILI9341_INVOFF)

    def backlite(self, onoff):
        if self._led is not None:
            self._gpio.output(self._led, onoff)

    def image_to_data(self, image):
        """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
        # Source of this code: Adafruit ILI9341 python project
        pixels = image.convert('RGB').load()
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r,g,b = pixels[(x,y)]
                #color = color565(r, g, b)
                color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                yield (color >> 8) & 0xFF
                yield color & 0xFF



# We import these extra functions below as new custom methods of the PIL "draw" function:
# Hints on this custom method technique:
#     http://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc

def _textrotated(self, position, text, angle, font, fill="white"):
    # Define a function to create rotated text.
    # Source of this rotation coding: Adafruit ILI9341 python project
    # "Unfortunately PIL doesn't have good
    # native support for rotated fonts, but this function can be used to make a
    # text image and rotate it so it's easy to paste in the buffer."
    width, height = self.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the TFT canvas image, using text itself as a mask for transparency.
    Buffer.paste(rotated, position, rotated)  # into the global Buffer
    #   example:  draw.textrotated(position, text, angle, font, fill)

def _pasteimage(self, filename, position):
    Buffer.paste(Image.open(filename), position)
    # example: draw.pasteimage('bl.jpg', (30,80))

def _textwrapped(self, position, text1, length, height, font, fill="white"):
    text2=textwrap.wrap(text1, length)
    y=position[1]
    for t in text2:
        self.text((position[0],y), t, font=font, fill=fill)
        y += height
    # example:  draw.textwrapped((2,0), "but a lot longer", 50, 18, myFont, "black")

#        All colours may be any notation:
#        (255,0,0)  =red    (R, G, B)
#        0x0000FF   =red    BBGGRR
#        "#FF0000"  =red    RRGGBB
#        "red"      =red    html colour names, insensitive
