#!/usr/bin/env python
import time
from daemonize import Daemonize

pid = "/tmp/HUD.pid"
import math

from microdotphat import clear, set_pixel, show 


def main():
 while True:
    clear()
    t = time.time() * 10
    for x in range(45):
        y = int((math.sin(t + (x/2.5)) + 1) * 3.5)
        set_pixel(x, y, 1)
        
    show()
    time.sleep(0.01)

daemon = Daemonize(app="HUD", pid=pid, action=main)
daemon.start()
