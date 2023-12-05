import network
import requests 
import json
import time

class WLANComms:
    
    def __init__(self, wlan_config):
        self.wlan = network.WLAN(network.STA_IF)
        self.connected = False
        self.wlan_config = wlan_config
        
    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(self.wlan_config["ssid"], self.wlan_config["pw"])

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
                self.reconnect()

        return None
        
    
