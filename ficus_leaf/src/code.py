# Write your code here :-)
import board
import busio
import neopixel
import time
import random
import adafruit_ahtx0
import adafruit_ssd1306

TICK_INTERVAL = .1

#setup neopixel strip
signal = neopixel.NeoPixel(board.NEOPIXEL, 8, brightness=0.1, auto_write=False)

strip_len = 8
strip = neopixel.NeoPixel(board.D2, 8, brightness=0.1, auto_write=False)
strip.fill((0,0,0))
strip.show()

RED = (100,0,0)
BLUE = (0,0,100)
DARK_RED = (255,0,0)
DARK_BLUE = (0,0,255)

#keyboards uart output (to monitor for activity)
kb_uart = busio.UART(board.TX, board.RX, baudrate=38400, timeout=.01)

# Create sensor object, communicating over the board's default I2C bus
i2cAHT = board.STEMMA_I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2cAHT)

i2cOLED = board.STEMMA_I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2cOLED)

#temp/humid setup
f_max = 0.0
f_min = 1000.0
h_min = 100.0
h_max = 0
spinner = -1


def main_loop():

    signal_toggle = False
    strip_time = time.monotonic()
    signal_time = time.monotonic()
    swipe_toggle = False
    action_stren =  155
    counter = 0
    env_time = 0
    while (1):
        now = time.monotonic()

        #check for keyboard activity
        if kb_uart.in_waiting > 0:
            data = kb_uart.read()
            #make the strip brighter
            action_stren=100

        #is it time to move the lights?
        if(now - strip_time) > TICK_INTERVAL:
            #decay the action strenghth over time
            if action_stren > 0:
                action_stren-=10
            else:
                action_stren = 0

            index = counter

            if swipe_toggle:
                index = (strip_len-1) - counter

            strip.fill((0,0,75+action_stren))
            strip[index] = (75+action_stren,0,0)
            strip.show()
            strip_time = now

            counter+=1
            if counter >= strip_len:
                counter = 1
                swipe_toggle = not swipe_toggle

        #update the board lights
        elif(now - signal_time > 1):
            if signal_toggle:
                signal_toggle = False
                signal.fill((255, 0, 0))
                signal.show()
            else:
                signal_toggle = True
                signal.fill((0, 0, 255))
                signal.show()
            signal_time = now

        elif(now - env_time > 5):
            env_time = now
            checkEnv()

def randlights():
    while(1):
        strip.fill((0,0,255))
        for i in range(strip_len):
            if random.random() > .5:
                strip[i]=((255,0,0))
        time.sleep(.25)
        strip.show()


def checkEnv():
    global f_max
    global f_min
    global h_min
    global h_max
    global spinner

    c = sensor.temperature
    f = (c * 1.8) + 32
    h = sensor.relative_humidity
    t_str = "Temp: %0.1fF - %0.1fC" % (f, c)
    h_str = "Humid: %0.1f%%" % h
    print(t_str)
    print(h_str)

    if f > f_max:
        f_max = f

    if f < f_min:
        f_min = f

    if h > h_max:
        h_max = h

    if h < h_min:
        h_min = h

    spinner_text = ""

    spinner += 1
    if spinner == 0:
        spinner_text = "Max F: %0.1f" % f_max
    elif spinner == 1:
        spinner_text = "Min F: %0.1f" % f_min
    elif spinner == 2:
        spinner_text = "Max H: %0.1f%%" % h_max
    elif spinner == 3:
        spinner_text = "Min H: %0.1f%%" % h_min
    elif spinner == 4:
        spinner = -1

    oled.fill(0)

    oled.text(t_str, 0, 0, 1)
    oled.text(h_str, 0, 10, 1)
    oled.text(spinner_text, 0, 25, 1)
    oled.show()


#everything is setup, let's start swiping!
main_loop()

