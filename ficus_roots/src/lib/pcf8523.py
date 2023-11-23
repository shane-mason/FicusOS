# The MIT License (MIT)
#
# Copyright (c) 2016 Philip R. Moyer and Radomir Dopieralski for Adafruit Industries.
#
""" PCF8523 Real Time Clock (RTC) module for MicroPython

Jun. 2020 Meurisse D. for MCHobby (shop.mchobby.be) - backport to MicroPython
Nov. 2016 Philip R. Moyer and Radomir Dopieralski for Adafruit Industries - original version for CircuitPython

- Milliseconds are not supported by this RTC.
- Datasheet: http://cache.nxp.com/documents/data_sheet/PCF8523.pdf
- based on https://github.com/adafruit/Adafruit_CircuitPython_PCF8523.git
"""

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/pcf8523"

import time

STANDARD_BATTERY_SWITCHOVER_AND_DETECTION = 0b000
BATTERY_SWITCHOVER_OFF = 0b111

RTC_REG = 0x03
ALARM_REG = 0x0A

def _bcd2bin(value):
    """Convert binary coded decimal to Binary """
    return value - 6 * (value >> 4)


def _bin2bcd(value):
    """Convert a binary value to binary coded decimal."""
    return value + 6 * (value // 10)

class PCF8523:
    """Interface to the PCF8523 RTC."""

    def __init__(self, i2c ):
        self.i2c = i2c
        self.address = 0x68
        self.buf1 = bytearray(1)
        self.buf7 = bytearray(7)

        # Try and verify this is the RTC we expect by checking the timer B
        # frequency control bits which are 1 on reset and shouldn't ever be
        # changed.
        self.buf1[0] = 0x12
        self.i2c.writeto( self.address, self.buf1 )
        self.i2c.readfrom_into( self.address, self.buf1 )

        if (self.buf1[0] & 0b00000111) != 0b00000111:
            raise ValueError("Unable to find PCF8523 at i2c address 0x68.")

    def _read_datetime( self, time_reg ):
        """Gets the date and time from a given register location (0x03 for RTC, 0x0A for alarm )."""
        weekday_offset = 1
        weekday_start  = 0

        self.buf1[0] = time_reg
        self.i2c.writeto( self.address, self.buf1 )
        self.i2c.readfrom_into( self.address, self.buf7 )
        #CircuitPython struct_time (tm_year=1999, tm_mon=12, tm_mday=31, tm_hour=17, tm_min=4, tm_sec=58, tm_wday=4, tm_yday=365, tm_isdst=0)
        #MicroPython mktime (year, month, mday, hour, minute, second, weekday, yearday)
        return time.mktime((
                _bcd2bin(self.buf7[6]) + 2000,
                _bcd2bin(self.buf7[5]),
                _bcd2bin(self.buf7[4 - weekday_offset]),
                _bcd2bin(self.buf7[2]),
                _bcd2bin(self.buf7[1]),
                _bcd2bin(self.buf7[0] & 0x7F),
                _bcd2bin(self.buf7[3 + weekday_offset] - weekday_start),
                -1,
                -1,  ))

    def _write_datetime( self, time_reg, value ):
        """ set the time from the tuple (year, month, mday, hour, minute, second, weekday, yearday) on the given register (0x03 for RTC, 0x0A for alarm)"""
        weekday_offset = 1
        weekday_start  = 0

        self.buf7[0] = _bin2bcd(value[5]) & 0x7F  # tm_sec format conversions
        self.buf7[1] = _bin2bcd(value[4]) # tm_min
        self.buf7[2] = _bin2bcd(value[3]) # tm_hour
        self.buf7[3 + weekday_offset] = _bin2bcd(
            value[6] + weekday_start # tm_wday
        )
        self.buf7[4 - weekday_offset] = _bin2bcd(value[2]) # tm_mday
        self.buf7[5] = _bin2bcd(value[1]) # tm_mon
        self.buf7[6] = _bin2bcd(value[0] - 2000) # tm_year

        self.i2c.writeto_mem( self.address, time_reg, self.buf7 )

    @property
    def datetime(self):
        """Gets or Set the current date and time then starts the clock."""
        return self._read_datetime( RTC_REG )

    @datetime.setter
    def datetime(self, value ):
        """ set the current time from the tuple (year, month, mday, hour, minute, second, weekday, yearday) """
        # Automatically sets lost_power to false.
        self.power_management = STANDARD_BATTERY_SWITCHOVER_AND_DETECTION

        self._write_datetime( RTC_REG, value )

    @property
    def power_management(self):
        """ Power management state that dictates battery switchover, power sources
            and low battery detection. Defaults to BATTERY_SWITCHOVER_OFF (0b000). """
        # i2c_bits.RWBits(3, 0x02, 5)
        self.i2c.readfrom_mem_into( self.address, 0x02, self.buf1 )
        return self.buf1[0] >> 5

    @power_management.setter
    def power_management(self, value ):
        # reg 0x02 bits 5,6,7 (3 lasts bits)
        self.i2c.readfrom_mem_into( self.address, 0x02, self.buf1 )
        self.buf1[0] = self.buf1[0] & 0b00011111
        self.buf1[0] = self.buf1[0] | (value << 5)
        self.i2c.writeto_mem( self.address, 0x02, self.buf1 )

    @property
    def lost_power( self ):
        """ True if the device has lost power since the time was set."""
        self.i2c.readfrom_mem_into( self.address, 0x03, self.buf1 )
        return (self.buf1[0] & 0b10000000) == 0b10000000

    @lost_power.setter
    def lost_power( self, value ):
        self.i2c.readfrom_mem_into( self.address, 0x03, self.buf1 )
        self.buf1 = (self.buf1[0] & 0b01111111) # Clear the bit
        if value:
            self.buf1 = self.buf1[0] | 0b10000000
        self.i2c.writeto_mem( self.address, 0x03, self.buf1 )

    @property
    def battery_low( self ):
        """ True if the battery is low and should be replaced."""
        self.i2c.readfrom_mem_into( self.address, 0x02, self.buf1 )
        return (self.buf1[0] & 0b00000100 ) == 0b00000100

    @property
    def alarm_interrupt( self ):
        """ True if the interrupt pin will output when alarm is alarming. """
        self.i2c.readfrom_mem_into( self.address, 0x00, self.buf1 )
        return ( self.buf1[0] & 0b00000010 ) == 0b00000010

    @alarm_interrupt.setter
    def alarm_interrupt( self, value ):
        self.i2c.readfrom_mem_into( self.address, 0x00, self.buf1 )
        self.buf1[0] = self.buf1[0] & 0b11111101 # clear the bit
        if value:
            self.buf1[0] = self.buf1[0] | 0b00000010 # set the bit
        self.i2c.writeto_mem( self.address, 0x00, self.buf1 )

    @property
    def alarm_status( self ):
        """ True if alarm is alarming. Set to False to reset """
        self.i2c.readfrom_mem_into( self.address, 0x01, self.buf1 )
        return ( self.buf1[0] & 0b00001000 ) == 0b00001000

    @alarm_status.setter
    def alarm_status( self, value ):
        self.i2c.readfrom_mem_into( self.address, 0x01, self.buf1 )
        self.buf1[0] = self.buf1[0] & 0b11110111 # clear the bit
        if value:
            self.buf1[0] = self.buf1[0] | 0b00001000 # set the bit
        self.i2c.writeto_mem( self.address, 0x01, self.buf1 )

    def alarm_min( self, min=None, enable=None ):
        """ get or set the alarm minute """
        # read current definition
        self.i2c.readfrom_mem_into( self.address, ALARM_REG + 0x00, self.buf1 )
        if min==None and enable==None:
            min = _bcd2bin( self.buf1[0] & 0b01111111 )
            enable = not((self.buf1[0] & 0b10000000) == 0b10000000) # Register @ 0 when enabled
            return min,enable
        else:
            if min!=None:
                self.buf1[0] = self.buf1[0] & 0b10000000 # keep enable info
                self.buf1[0] = self.buf1[0] | (_bin2bcd(min) & 0b01111111) # inject min
            if enable!=None:
                enable = not(enable) # alarm is enabled when 0 is placed into the register
                self.buf1[0] = self.buf1[0] & 0b01111111 # keep min info
                if enable:
                    self.buf1[0] = self.buf1[0] | 0b10000000 # Inject enable
            self.i2c.writeto_mem( self.address, ALARM_REG + 0x00, self.buf1 )

    def alarm_hour( self, hour=None, enable=None ):
        """ get or set the alarm hour """
        # read current definition
        self.i2c.readfrom_mem_into( self.address, ALARM_REG + 0x01, self.buf1 )
        if hour==None and enable==None:
            hour = _bcd2bin( self.buf1[0] & 0b00111111 )
            enable = not((self.buf1[0] & 0b10000000) == 0b10000000) # Register @ 0 when enabled
            return hour,enable
        else:
            if hour!=None:
                self.buf1[0] = self.buf1[0] & 0b10000000 # keep enable info
                self.buf1[0] = self.buf1[0] | (_bin2bcd(hour) & 0b00111111) # inject hour
            if enable!=None:
                enable = not(enable) # alarm is enabled when 0 is placed into the register
                self.buf1[0] = self.buf1[0] & 0b01111111 # keep min info
                if enable:
                    self.buf1[0] = self.buf1[0] | 0b10000000 # Inject enable
            self.i2c.writeto_mem( self.address, ALARM_REG + 0x01, self.buf1 )


    def alarm_day( self, day=None, enable=None ):
        """ get or set the alarm day """
        # read current definition
        self.i2c.readfrom_mem_into( self.address, ALARM_REG + 0x02, self.buf1 )
        if day==None and enable==None:
            day = _bcd2bin( self.buf1[0] & 0b00111111 )
            enable = not((self.buf1[0] & 0b10000000) == 0b10000000) # Register @ 0 when enabled
            return day,enable
        else:
            if day!=None:
                self.buf1[0] = self.buf1[0] & 0b10000000 # keep enable info
                self.buf1[0] = self.buf1[0] | (_bin2bcd(day) & 0b00111111) # inject day
            if enable!=None:
                enable = not(enable) # alarm is enabled when 0 is placed into the register
                self.buf1[0] = self.buf1[0] & 0b00111111 # keep day info
                if enable:
                    self.buf1[0] = self.buf1[0] | 0b10000000 # Inject enable
            self.i2c.writeto_mem( self.address, ALARM_REG + 0x02, self.buf1 )


    def alarm_weekday( self, weekday=None, enable=None ):
        """ get or set the alarm day """
        # read current definition
        self.i2c.readfrom_mem_into( self.address, ALARM_REG + 0x03, self.buf1 )
        weekday_start  = 0
        if weekday==None and enable==None:
            weekday = _bcd2bin( (self.buf1[0] & 0b00000111) - weekday_start )
            enable = not((self.buf1[0] & 0b10000000) == 0b10000000) # Register @ 0 when enabled
            return weekday,enable
        else:
            if weekday!=None:
                self.buf1[0] = self.buf1[0] & 0b10000000 # keep enable info
                self.buf1[0] = self.buf1[0] | (_bin2bcd(weekday) & 0b00000111) # inject weekday
            if enable!=None:
                enable = not(enable) # alarm is enabled when 0 is placed into the register
                self.buf1[0] = self.buf1[0] & 0b00000111 # keep weekday info
                if enable:
                    self.buf1[0] = self.buf1[0] | 0b10000000 # Inject enable
            self.i2c.writeto_mem( self.address, ALARM_REG + 0x03, self.buf1 )
