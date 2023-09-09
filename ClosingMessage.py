from Displays import *

class ClosingMessage:

    def __init__(self):
        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)  
    
    def run(self):    
        self._display.showText("Thanks for playing Player 1")
        self._display.reset()
        self._display.showText("Good Bye!")
    
