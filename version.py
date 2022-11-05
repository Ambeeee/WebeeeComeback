from datetime import datetime
from pyperclip import copy as cp

def get_version():
    date = datetime.now().strftime("%y%m%d")
    time = datetime.now().strftime("%H:%M")
    version = f"V {date} {time}"
    return version


cp(get_version())
print("Copiato negli appunti!")
print(get_version())