#!/usr/bin/env python3
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key


class AutoClicker(threading.Thread):
    def __init__(self):
        super(AutoClicker, self).__init__()
        self.button = Button.right
        self.cps = 5 # max 60 cps but not always \ comment out delay to max out cps
        self.delay = (1 / self.cps) - (1 / self.cps) / 4.5
        self.clicking = False
        self.block = False

    def change_clicking(self):
        self.clicking = not self.clicking

    def run(self):
        while True:
            time.sleep(0.00001)
            while self.clicking:
                mouse.click(self.button)
                time.sleep(self.delay) # comment out this to max out cps


mouse = Controller()
ac = AutoClicker()
ac.start()

def on_press(key):
    #key = str(key)
    #key = key.replace("'", '')
    if key == Key.ctrl_r:
        ac.block = not ac.block
    if key == Key.caps_lock and not ac.block:
        ac.change_clicking()


with Listener(on_press=on_press) as listener:
    listener.join()
