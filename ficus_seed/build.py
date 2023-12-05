#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import os
PORT = "COM6"
files = []
os.chdir("src")

from pathlib import Path

p = Path(".")

files = list(p.glob('**/*.py'))


for file in files:
    fn = str(file).replace("\\", "/")
    command = f"ampy --port {PORT} put {fn} {fn}"
    print(f"Running: {command}")
    os.system(command)

