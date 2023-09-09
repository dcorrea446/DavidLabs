import time
from Lights import *

class Pattern:
    def __init__(self):
        self._ledR = Light(22, "Red LED")
        self._ledB = Light(27, "Blue LED")
    
    def run(self): 
        self._ledR.on()
        utime.sleep(2)
        self._ledB.on()
        utime.sleep(2)
        self._ledR.off()
        utime.sleep(2)
        self._ledB.off()
   