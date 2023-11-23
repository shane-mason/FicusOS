#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import os
PORT = "COM7"
files = [ "main.py", "sd_setup.py", "lib/sdcard.py", "lib/ficus/ficus_shell.py", "lib/ficus/fshell_deadletter.py",  "lib/ficus/fshell_stateless.py" ]

for file in files:
    command = f"ampy --port {PORT} get {file} src/{file}"
    print(f"Running: {command}")
    os.system(command)