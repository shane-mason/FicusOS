
# FicusOS Leaf
Lightshow and environmental monitor for FicusOS

## Hardware requirements

* Sparkfun RP2040 Pro Micro (or similar)
* Neopixel chain
* 1306 OLED

## Install prerequisites

Requires Adafruit's CircuitPython 

## Install Libraries from Adafruit Bundle
Requires Adafruit Circuit Python libraries from their bundle of 'mpy' libraries.

[GitHub Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle)

Copy the following into the devices lib/ folder

```
adafruit_bus_device/ (folder)
adafruit_bus_device.mpy
adafruit_ahtx0.mpy
adafruit_displayio_ssd1306.mpy
adafruit_framebuf.mpy
adafruit_pixelbuf.mpy
adafruit_ssd1306.mpy
neopixel.mpy
```

## Deploy to Device

Circuit Python devices will mount like an sdcard, so you can simply copy the single file `code.py` over to the device. See [Circuit Python Drives](https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive) for more information.

Esnure that font5x8.bin is included next to code.py.