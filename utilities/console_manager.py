import os
import sys


def clear():
    try:
        if sys.platform.index("linux") >= 0:
            os.system("clear")
    except:
        os.system("cls")


def gotoxy(x, y, obj=""):
    print("%c[%d;%df" % (0x1B, y, x), end="")
    print(obj)
