# FicusOS Trunx
Ficus is built on a 1-bit data bus, and most nodes are restricted to two UART connections at a time. This node is a primary routing node that is responsible for routing messages to the correct destination. In most cases, it broadcasts out to multiple listeners per channel. It listens directly to the USB input node and communicates bi-directionally with the shell node. For the reference implementation, this node runs on a Raspberry Pico RP2040. The code is implemented in C using the Raspberry Pico SDK.

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