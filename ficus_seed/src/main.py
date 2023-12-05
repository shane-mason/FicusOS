import machine
import sys
import time
import aht
import framebuf
import ssd1306
import rp2
from wlancomms import WLANComms
from ficus_piezo import FicusPiezo

FICUS_ID = "Remote"
DISP_WIDTH = 128
DISP_HEIGHT = 64
USE_F = True

#hello world
wlan_config = {
    "ssid": "Maui",
    "pw": "loki2014"
    }

server_config = {
    "time_url": "http://192.168.1.187:5000/time",
    "env_url": "http://192.168.1.187:5000/env"
    
}

class EnvironDiplay:
    
    def __init__(self):
        self.disp = None    
        disp_i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16),freq=200000)

        self.disp = ssd1306.SSD1306_I2C(DISP_WIDTH, DISP_HEIGHT, disp_i2c)
        self.disp.fill(0)
        self.disp.text("Ficus up.", 0, 0)
        self.disp.show()
        self.stats_spinner = 0


    def update_stats(self, stats):
        
        h_string = "Humid: {:.1f}%".format(stats.h)
        stat_string = ""
        t_string = ""
        if USE_F:
            f = (stats.c*1.8) + 32
            t_string = f"Temp:  {f:.1f}F"
        else:
            t_string = f"Temp:  {stats.c:.1f}C"
        

        if self.stats_spinner == 0:
            if USE_F:
                f = (stats.cmax*1.8) + 32
                stat_string = f"F Max: {f:.1f}F"
            else:
                stat_string = f"C Max: {stats.maxc:.1f}C"
        elif self.stats_spinner == 1:
            if USE_F:
                f = (stats.cmin*1.8) + 32
                stat_string = f"F Min: {f:.1f}F"
            else:
                stat_string = f"C Min: {stats.cmin:.1f}C"
        elif self.stats_spinner == 2:
            stat_string = f"H Max: {stats.hmax:.1f}%"
        elif self.stats_spinner == 3:
            stat_string = f"H Min: {stats.hmin:.1f}%"
        
        self.stats_spinner+=1
        if self.stats_spinner >= 5:
            self.stats_spinner = 0
        
        time_str = self._time_str()
        
        self.disp.fill(0)
        self.disp.text(time_str, 0, 2)
        self.disp.text(t_string, 0, 20)
        self.disp.text(h_string, 0, 35)
        self.disp.text(stat_string, 0, 50)
        self.disp.show()

    def _time_str(self):
        (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
        return  f"{month}/{mday} - {hour:02d}:{minute:02d}:{second:02d}"

    def show_notice(self, text, duration_ms=0):
        self.disp.fill(0)
        self.disp.text(text, 0, 2)
        self.disp.show()
        if duration_ms:
            time.sleep_ms(duration_ms)
        
    def check_reset(self):
        do_reset = True
        
        #check that button is pressed for 5 seconds
        for i in range(5, 0, -1):
            if rp2.bootsel_button():
                prompt = "Reset Stats? " + str(i)
                self.show_notice(prompt, 1000)
            else:            
                do_reset = False
                break;
            
        if do_reset:
            self.show_notice("Resetting now :)", 1500)
            #if they keep pushing the button, it will enter reset again
            if rp2.bootsel_button():
                self.show_notice("Let go :)", 1500)
        else:
            self.show_notice("Wont reset :)", 500)

        return do_reset


class EnvironStats:
    
    def __init__(self, c, h):
        self.cmax = c
        self.cmin = c
        
        self.hmax = h
        self.hmin = h
        self.c = c
        self.h = h

    def update(self, c, h):
        self.c = c
        self.h = h
        if c > self.cmax:
            self.cmax = c
        if c < self.cmin:
            self.cmin = c
        if h > self.hmax:
            self.hmax = h
        if h < self.hmin:
            self.hmin = h
        
    def reset(self, c, h):
        self.c = c
        self.h = h
        self.cmax = c
        self.cmin = c
        self.hmax = h
        self.hmin = h

def sync_server_time():
    server_time = wlan.get_url(server_config['time_url'])
    if server_time != None:
        print(server_time)     
        now = (server_time["year"], server_time["month"], server_time["day"], server_time["wday"],
               server_time["hour"], server_time["minute"], server_time["second"], 0)
        rtc = machine.RTC()
        rtc.datetime(now)
    else:
        print ("Got nothing back...")
    
sensor_i2c = machine.I2C(1, scl=machine.Pin(15), sda=machine.Pin(14))
sensor = aht.AHT2x(sensor_i2c, crc=True)


disp = EnvironDiplay()

check_count = 0

while not sensor.is_ready:
    check_count+=1
    disp.show_notice("Checking Env Sensor:" % check_count, 1000);
    
    if check_count >= 5:
        disp.show_notice("Sensor not online.", 1000);
        break
    
stat_keeper = EnvironStats(sensor.temperature, sensor.humidity)
disp.show_notice("Connecting...")
wlan = WLANComms(wlan_config);
wlan.connect()
print("Connected - syncing time")
sync_server_time()
print("Time sync'ed")
FicusPiezo.play_start_seq()
while True:
    #setup tick start
    tick_start = time.ticks_ms()
    
    # reset history if bootsel pressed
    if rp2.bootsel_button():
        do_reset = disp.check_reset()
        if do_reset:
            stat_keeper.reset(sensor.temperature, sensor.humidity)
    
    if(time.time()%5==0):
        if sensor.is_ready:
            c = sensor.temperature
            h = sensor.humidity
            stat_keeper.update(c,h)
            disp.update_stats(stat_keeper)
            wlan.get_url(server_config['env_url'] + f"/{FICUS_ID}/{c}/{h}")

    if(time.time()%100==0):
        pass
        
    tick_end = time.ticks_ms()
    tick_time = time.ticks_diff(tick_end, tick_start)
    ms_to_sleep = 1000 - tick_time
    time.sleep_ms(ms_to_sleep);

    
