import time
import random
import utime
from Lights import *
from PlayerInput import *
from MemoryGameController import *

class SequenceGenerator:
    def __init__(self, dimlightG, dimlightR, dimlightB):
        self._sequence = []
        self._sequence_displayed = False
        self._sequence_start_time = 0
        self._sequence_display_time = 1000  # Reduced display time for quicker gameplay
        self._dimlightG = dimlightG
        self._dimlightR = dimlightR
        self._dimlightB = dimlightB

    def get_sequence(self):
        return self._sequence

    def generate_sequence(self):
        colors = ['G', 'R', 'B']
        previous_color = None  # Initialize previous color as None
        self._sequence = []
        
        for _ in range(5):  # Generate a sequence of 5 steps
            color = random.choice([c for c in colors if c != previous_color])
            self._sequence.append(color)
            previous_color = color
        
        self._sequence_displayed = False
        self.display_sequence()
        self._sequence_start_time = utime.ticks_ms()

    def display_sequence(self):
        for color in self._sequence:
            if color == 'G':
                self._dimlightG.on()
            elif color == 'R':
                self._dimlightR.on()
            elif color == 'B':
                self._dimlightB.on()
            time.sleep(1)  # Display each color for 1 second
            self._dimlightG.off()
            self._dimlightR.off()
            self._dimlightB.off()

    def reset_sequence(self):
        self._sequence = []
        self._sequence_displayed = False
        self._sequence_start_time = 0

    def next_round(self):
        self.reset_sequence()
        self.generate_sequence()
