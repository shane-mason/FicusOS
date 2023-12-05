#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import os
PORT = "COM6"
files = [ "main.py", "lib/wlancomms.py" ]

for file in files:
    command = f"ampy --port {PORT} get {file} src/{file}"
    print(f"Running: {command}")
    os.system(command)