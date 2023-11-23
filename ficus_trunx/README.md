# FicusOS Trunx
Basic routing module.

## Install Prerequisites

Requires Rasberry Pico SDK: https://www.raspberrypi.com/documentation/microcontrollers/c_sdk.html

## Build

```
mkdir build
cd build
cmake ..
```

The easiest way is to get VSCode pre-loaded for pico SDK and run build from the menu.

## Install

Use the bootsel button to put the pico in flash mode, copy build/ficus_trunx.uf2 to the bootloader.