#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import uasyncio as asyncio
from machine import UART, I2C, Pin, RTC
import time
import network
import urequests as requests
import json
from pcf8523 import PCF8523
from ficus.server_vine import ServerVine
from ficus.secrets import wlan_config


server_config = {
    "time_url": "http://192.168.1.187:5000/time"
    }

comm_pins = {
    "servtx" : 12,
    "servrx" : 13,
}

class FicusServer():
    
    def __init__(self, outq, outq_lock):
        self.led = Pin("LED", Pin.OUT)
        self.wlan = WLANComms()
        self.rtc = None
        self.outq = outq
        self.outq_lock = outq_lock
        i2c = I2C(0, sda=Pin(20), scl=Pin(21))
        self.pcf = PCF8523( i2c )
        self.vine = ServerVine(0, 38400, rxpin=comm_pins['servrx'], txpin=comm_pins['servtx'])
        
    
    async def run_forever(self):
        print("Starting wlan")
        await self.sync_persistent_time()
        await self.wlan.connect()
        if self.wlan.connected:
            
            await self.sync_server_time()
            now = self.rtc.datetime()
            print(now)
            
            
        _minute_tick = time.ticks_ms()
        
        while True:
            _tick = time.ticks_ms()
            
            self.led.toggle()
            #asyncio.create_task(self._tick_kb())
            
            if time.ticks_diff(_tick, _minute_tick) >= 12000:
                now = self.rtc.datetime()
                print("Sending Time: ", now)
                self.vine.send_time_sync(now)
                _minute_tick = _tick

    async def sync_persistent_time(self):
        print("Sync persistent time")
        now = self.pcf.datetime
        print(now)
        try:     
            if not self.rtc:
                self.rtc = RTC()
            (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime(now)
            #goes to: (year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
            self.rtc.datetime((year, month, mday, weekday, hour, minute, second, 0))
            
        except:
            print("Error syncing from persistent time.")

    async def sync_server_time(self):
        print("Sync server time")
        self.server_time = self.wlan.get_url(server_config['time_url'])
        if self.server_time != None:
            print(self.server_time)     
            now = (self.server_time["year"], self.server_time["month"], self.server_time["day"], self.server_time["wday"],
                   self.server_time["hour"], self.server_time["minute"], self.server_time["second"], 0)
            self.rtc = RTC()
            self.rtc.datetime(now)
            #sync time to persistent time
            #(year, month, mday, hour, minute, second, weekday, yearday)
            nowPcf = (self.server_time["year"], self.server_time["month"], self.server_time["day"], self.server_time["hour"],
                      self.server_time["minute"], self.server_time["second"], self.server_time["wday"], self.server_time["yday"])
            print("Setting time: " + str(time.time()))
            self.pcf.datetime = (nowPcf)
            
        else:
            print ("Got nothing back...")
            
    async def send_time_update(self):
        pass

class WLANComms:
    
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.connected = False
        
    async def connect(self):
        self.wlan.active(True)
        self.wlan.connect(wlan_config["ssid"], wlan_config["pw"])

        # Wait for connection to establish
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)
            
        # Manage connection errors
        if self.wlan.status() != 3:
            raise RuntimeError('Network Connection has failed')
        else:
            self.connected = True
            print('connected')
            
    async def reconnect(self):
        self.wlan.disconnect()
        self.connected = False
        await self.connect()
            
    def get_url(self, url):
        try:
            data=requests.get(url)
            as_json=data.json()
            data.close()            
            return as_json
        except:

            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                asyncio.create_task(self.reconnect())

        return None
        
    
