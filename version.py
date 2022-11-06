from datetime import datetime
from pyperclip import copy as cp

VERSION = "version.txt"

def recorded_version(mode="r", v=""):
    with open(VERSION, mode) as f:
        if mode == "r":
            last = f.read()
            return last
        elif mode == "w":
            f.write(v)

def new_version(j=""):
    date = datetime.now().strftime(j.join(["%y","%m","%d"]))
    time = datetime.now().strftime("%H:%M")
    version = f"V {date} {time}"
    return version

recorded_version("w", new_version("-"))
cp(new_version())
print("Copiato negli appunti!")
print(recorded_version()) 