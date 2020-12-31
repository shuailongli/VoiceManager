from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

import sys
argument=sys.argv[1]
Commandlist=["Key.page_up","Key.page_down","Key.up","Key.down"]
KeyControllerList=[Key.page_up,Key.page_down,Key.up,Key.down]
if argument in Commandlist:
    keystroke=KeyControllerList[Commandlist.index(argument)]
keyboard = KeyboardController()
keyboard.press(keystroke)
