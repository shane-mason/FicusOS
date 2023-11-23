#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
from machine import UART, Pin
from time import time_ns
from micropython import const

VINE_TIME_SYNC = const(220)
VINE_END = const(255)

class ServerVine:
 
    uart_id = 0
    baud_rate = 38400
    timeout = 50 # milliseconds
    
    def __init__(self, uart_id:int, baud_rate:int=None, txpin=12, rxpin=13, ):
        self.uart_id = uart_id
        if baud_rate: self.baud_rate = baud_rate

        # set the baud rate
        self.uart = UART(self.uart_id,self.baud_rate, tx=Pin(txpin), rx=Pin(rxpin))

        # Initialise the UART serial port
        self.uart.init()
        
    def send_time_sync(self, now):
        (year, month, day, weekday, hours, minutes, seconds, subseconds) = now
        #embedded Y3K bug right here:
        year-=2000
        msg = bytes([VINE_TIME_SYNC, year, month, day, weekday, hours, minutes, seconds, subseconds, VINE_END])
        self.uart.write(msg)
    