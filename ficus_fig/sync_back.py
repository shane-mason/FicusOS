import os
PORT = "COM7"
files = [ "main.py", "sd_setup.py", "lib/sdcard.py", "lib/ficus/ficus_shell.py", "lib/ficus/ficus_deadletter.py",  "lib/ficus/ficus_stateless.py" ]

for file in files:
    command = f"ampy --port {PORT} get {file} src/{file}"
    print(f"Running: {command}")
    os.system(command)