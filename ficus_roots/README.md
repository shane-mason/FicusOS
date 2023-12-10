# Ficus Roots
Roots reach outward, and this node provides essential networking support to the Ficus reference implementation. On startup, it connects to the Ficus Web App, requests a time update, and distributes that time across the data bus. If not online, it will read the current time from a battery-backed PCF8523 Realtime Clock breakout on an i2c connection and distribute that time. Since the PCF8523 is known to drift, the Roots node will overwrite PCF8523 time with network time when received. This node is implemented in MicroPython for flexibility.

In the image below, the Roots node is on the right side.

![Basic reference implementation](../docs/img/ficus-middle.jpg)

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

### Add wifi password

The wifi configuration is stored in a Python file called lib/ficus/secrets.py - this is NOT saved to the repository for security reasons, so you will need to manually create it. It should have the following format:

```
wlan_config = {
    "ssid": "WIFI_SSID",
    "pw": "WIFI_PASSWORD"
}
```

where WIFI_SSID is replaced with your real wifi ssid and WIFI_PASSWORD with a valid password for that SSID.

### Sync back from board

If you work on the files on the board, using Thonny or equivalent, use this script to sync them back to your computer.