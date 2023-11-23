import machine
import os
import sdcard

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(13, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(14),
                  mosi=machine.Pin(15),
                  miso=machine.Pin(12))

# Initialize SD card
sd = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = os.VfsFat(sd)
os.mount(vfs, "/base")

# Create a file and write something to it
with open("/base/test01.txt", "w") as file:
    file.write("Hello, SD World!\n")
    file.write("This is a test\n")

# Open the file we just created and read from it
with open("/base/test01.txt", "r") as file:
    data = file.read()
    print(data)