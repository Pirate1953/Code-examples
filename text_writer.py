from time import sleep
import os

g = lambda com: os.system(com)
g('pip install pyautogui')
sleep(2)

import pyautogui
fname = input()
f = open(fname, 'r')
sleep(3)
pyautogui.typewrite(f.read())
