from datetime import datetime
from pyperclip import copy as cp

def get_version():
    time=datetime.now()
    date = time.strftime("%Y%m%d")
    hour = time.strftime("%H:%M")
    version = f"V {date} {hour}"
    return version

cp(get_version())
print("Copiato nella clipboard!")
print(get_version())