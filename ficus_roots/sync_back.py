#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import os
PORT = "COM6"
files = [ "main.py", "lib/pcf8523.py", "lib/ficus/secrets.py", "lib/ficus/ficus_piezo.py",  "lib/ficus/ficus_server.py", "lib/ficus/server_vine.py" ]

for file in files:
    command = f"ampy --port {PORT} get {file} src/{file}"
    print(f"Running: {command}")
    os.system(command)