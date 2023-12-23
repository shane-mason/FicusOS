#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import machine
from machine import UART, Pin, RTC
import time
import _thread
from ficus.ficus_shell import FShell
from micropython import const

#vine command constants - this should be imported...
VINE_TIME_SYNC = const(220)
VINE_END = const(255)

internal_led = machine.Pin(25, machine.Pin.OUT)

#setup threading
mlock = _thread.allocate_lock()
rtc = RTC()

#core0 monitors for incoming messages on UART0 - with is tied to the keys node (keyboard io generally)
def core0():
    uart0 = UART(0, 38400, rx=Pin(1), tx=Pin(0))
    fshell = FShell()
    while True:
        #mlock.acquire()
        #do something
        #mlock.release()
        
        if (uart0.any() > 0):
            message = uart0.read()
            if message[0] == 250 and message[-1] == 255:
                command = message[1:-1].decode('ascii')
                print("Got Message: ", command)
                resp = fshell.process_command(command)
                uart0.write(resp)
            else:
                print("Message not correctly formatted")

#core1 monitors for incoming requests on UART1
def core1():
    uart1 = UART(1, 38400, rx=Pin(9), tx=Pin(8))
    while True:
        internal_led.toggle()
        time.sleep(0.25)
        if uart1.any() > 0:
            msg = uart1.read()
            if msg[0] == VINE_TIME_SYNC and msg[-1] == VINE_END:
                #got the timesync message - need to fix the year for datetime
                y = msg[1] + 2000
                #Format: (year, month, day, weekday, hours, minutes, seconds, subseconds)
                mlock.acquire()
                rtc.datetime((y, msg[2], msg[3], msg[4], msg[5], msg[6], msg[7], msg[8]))
                mlock.release()
                

_thread.start_new_thread(core0, ())
core1()