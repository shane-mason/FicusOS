#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
from machine import RTC
import machine
import random
import os
from ficus.fshell_stateless import FShellStatic
from ficus.fshell_deadletter import FShellDeadletter
import sdcard

class FShell():
    
    def __init__(self):
        self.rtc = RTC()
        #os.chdir("/lib/base")
        
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
        self.sd = sdcard.SDCard(spi, cs)
        
        # Mount filesystem
        vfs = os.VfsFat(self.sd)
        os.mount(vfs, "/safe")
        
        os.chdir("/safe/base")
        
        print(", ".join(os.listdir()))
        
    def process_command(self, command):
        #try:
        tokens = command.split()
        resp = ""
        if hasattr(self, tokens[0]):
            resp = getattr(self, tokens[0])(tokens=tokens, context=None)
            print("Resp: ", resp)
            resp = b'\xf9' + bytes(resp, 'ascii') + b'\xff'
        elif hasattr(FShellStatic, tokens[0]):
            resp = getattr(FShellStatic, tokens[0])(tokens=tokens, context=None)
            resp = b'\xf9' + bytes(resp, 'ascii') + b'\xff'
        elif hasattr(FShellDeadletter, tokens[0]):
            resp = getattr(FShellDeadletter, tokens[0])(tokens=tokens, context=None)
            resp = b'\xf9' + bytes(resp, 'ascii') + b'\xff'    
        else:
            #last chance - check apps dir
            files = os.listdir("/safe/apps")
            print("Looking for:", tokens[0])
            found = False
            for filename in files:
                if tokens[0] == str(filename):
                    full_path = f"/safe/apps/{filename}"
                    fp = open(full_path, "r")
                    contents = fp.read()
                    print("Executing:", contents)
                    shared_state = {"shell_response": None, "tokens": tokens, "context": None}
                    exec(contents, {}, shared_state)
                    print("Shell Response: ", the_dict['shell_response'])
                    resp = b'\xf9' + bytes(the_dict['shell_response'], 'ascii') + b'\xff'
                    found = True
            if not found:
                resp = b'\xf8' + bytes("I couldn't find that.", 'ascii') + b'\xff';

        #except:
        #    resp = resp = b'\xf8' + bytes("Something weird happened.", 'ascii') + b'\xff';
            
        return resp

    def time(self, tokens=None, context=None):
        (y, mo, d, wd, h, mi, s, ss) = self.rtc.datetime()
        return f"{mo}.{d}.{y} {h}:{mi}:{s}.{ss}"
    
    def pwd(self, tokens=None, context=None):
        return os.getcwd()
    
    def cwd(self, tokens=None, context=None):
        return os.getcwd()
    
    def ls(self, tokens=None, context=None):
        resp = os.listdir()
        if len(resp) == 0:
            return "Empty Directory"
        return "\n".join(resp)
    
    def cd(self, tokens=None, context=None):
        os.chdir(tokens[1])
        nd = os.getcwd()
        return f"New location: {nd}"
    
    def rm(self, tokens=None, context=None):
        os.remove(tokens[1])
        return f"Removed: {tokens[1]}"
    
    def mkdir(self, tokens=None, context=None):
        os.mkdir(tokens[1])
        return f"Made Dir: {tokens[1]}"
    
    def rmdir(self, tokens=None, context=None):
        os.remove(tokens[1])
        return f"Removed Dir: {tokens[1]}"
    
    def head(self, tokens=None, context=None):
        f = open(tokens[1],"r")
        resp = ""
        for i in range(10):
            resp += f.readline()
        return resp
    
    def a(self, tokens=None, context=None):
        f = open(tokens[1],"a")
        print("Token:", tokens[1])
        line = " ".join(tokens[2:])
        print("Line:",line)
        
        f.write(line)
        f.write("\n")
        resp = f"Wrote to {tokens[1]}:\n{line}"
        f.close()
        return resp

    
        
        
    

    