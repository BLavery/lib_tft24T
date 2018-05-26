# lib_tft24T
2.4 inch 320x240 SPI LCD with Touchscreen - a Python Driver

## May 2018 - This is no longer being maintained by the original author.
## Please feel free to fork, copy, adapt if you find it useable

This module is currently popular on eBay. The marking says TJCTM24024-SPI. This is a ILI9341 driven LCD display, with XPT2046 chip for touch device, and it also includes a SD card holder. All sections are SPI.

My interest is for straightforward python library module(s) for LCD and Touch. The SD card I will ignore. My application is for Raspberry Pi, and for Virtual-GPIO after I check that out.

My LCD driver is NOT a framebuffer method. (320x240 is too tiny to format any normal desktop display onto.) Also it is NOT an instant direct write-to-LCD method. It instead uses the Python Image Library (PIL) to prepare all display content on a “canvas” or buffer. It gets a transfer of the total buffer to screen hardware when ready. This give some transfer delay, as 0.25MB gets transferred by SPI each screen update! So it's not invisibly “snappy”, but I find it quite acceptable for my requirement. The advantage of using PIL is that a well-tried and versatile graphics and text/font library is all usable directly. The disadvantage is that PIL is discontinued, I believe, and is not there for python3, only python 2.x. Its successor PILLOW seems still to be “coming” for Raspberry Pi. (Any correction to this??)

This implementation supports portrait (320Hx240W) and landscape (240Hx320W) modes fairly naturally to the user, despite that the hardware is inherently operating in portrait mode.

The hardware uses 5V for its Vcc power, but the logic levels are 3.3V max. (Vcc can be changed to 3.3 with a soldered link, but 5V is easy enough on the Pi.) I note several vague references on eBay supplier sites that 5V can be used for the logic I/O, but as far as I can see they are wrong.

For best screen update time, I have cranked up the SPI speed to 32,000,000 Hz, which seems to be maximum for the venerable old Rpi, but it is an option, and perhaps the Rpi2 may allow faster?

You need:
-  Raspberry Pi (duh), any version, and I used stock current Raspbian on a 256k early Rpi.
-  python2.7
-  PIL installed
-  SPIDEV installed
-  SPI enabled (Module blacklist? Device tree?)

For the LCD you need to connect this logic:
-  MOSI
-  SCLK
-  CS – I used CE0
-  D/C – to any GPIO pin – I used #22
-  RESET – to any GPIO pin (option: just tie it to 3.3) – I used #18
-  LED – to any GPIO pin (option: just tie it to 3.3) – I used #23
-  MISO – not used

For TOUCHSCREEN you need:
-  SCLK (again)
-  CE1
-  MOSI (again)
-  MISO
-  PEN-IRQ - to a GPIO pin - I used #24

Included are
-  a demo of using canvas mode to draw text & graphics to display
-  a calibration utility to find the correct scaling and offset factors matching touch device and screen pixels
-  a "penprint trail" demo of touch screen
-  a "GUI" calculator on the display, using stylus to operate.

Note that a finger does work on the touch device, but a stylus/pen works heaps better.



Brian
April 2015
