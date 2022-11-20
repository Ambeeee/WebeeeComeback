from datetime import datetime
from pyperclip import copy as cp

VERSION = "version.txt"

def recorded_version():
    with open(VERSION, "r") as f:
        last_v = f.read()
        return last_v

def new_version():
    date_to_print = datetime.now().strftime("%y%m%d")
    date_to_save = datetime.now().strftime("%y-%m-%d")
    time = datetime.now().strftime("%H:%M")
    version_to_print = f"V {date_to_print} {time}"
    version_to_save = f"V {date_to_save} {time}"

    with open(VERSION, "w") as f:
        f.write(version_to_save)

    return version_to_print

print(new_version())
try: cp(new_version())
except: pass
print("Copiato negli appunti!")