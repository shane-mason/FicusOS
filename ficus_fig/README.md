# FicusOS Fig
The FicusOS shell.

## Hardware Requirements

* Raspberry Pico W (or similar RP2040 with WLAN support)
* PCF8523 Realtime Clock breakout on i2c connection

## Install Prequisites

Install pyserial
```
pip install pyserial
```
Install ampy

```
pip install adafruit-ampy
```

Interacting with the persistent realtime-clock breakout requires PCF8523 support. We have included a 3rd party port from https://github.com/mchobby/esp8266-upy/tree/master/pcf8523 - feel free to overwrite with your own implementation for any other device.


### Build to board

Get com port to update build.py
```
python -m serial.tools.list_ports -v
```

Update PORT constant in build.py and sync_back.py

```
PORT=<SOME VALUE>
```

Deploy OS to board:

```python build.py```

### Sync back from board

If you work on the files on the board, using Thonny or equivalent, use this script to sync them back to your computer.