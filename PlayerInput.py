import time
from SequenceGenerator import *
from Model import *

class PlayerInput:
    def __init__(self, sequence_generator, buttonG, buttonR, buttonB, model, display, score):
        self._player_input = []  # Initialize player input as an empty list
        self._sequence_generator = sequence_generator
        self._buttonG = buttonG
        self._buttonR = buttonR
        self._buttonB = buttonB
        self._model = model
        self._display = display
        self._score = score  # Initialize score to 0

    def player_input(self):
        if len(self._player_input) < len(self._sequence_generator.get_sequence()):
            if self._buttonG.isPressed():
                self._player_input.append('G')
            elif self._buttonR.isPressed():
                self._player_input.append('R')
            elif self._buttonB.isPressed():
                self._player_input.append('B')
        else:
            # Compare player input to the generated sequence
            if self._player_input == self._sequence_generator.get_sequence():
                self._display.reset()
                self._display.showText('Correct! Well done!')
                time.sleep(1)
                self.update_score()
                self._display.reset()
                self._display.showText(f'Current Score: {self._score}')
                time.sleep(4)
  
            else:
                self._display.reset()
                self._display.showText('Incorrect! Try again.')
                time.sleep(1)
                self._display.reset()
                self._display.showText(f'Current Score: {self._score}')  
                time.sleep(4)
            # Start the next round with a new or different sequence
            # self._sequence_generator.next_round()

            # Reset player input
            self._player_input = []

            self._model.processEvent(TIMEOUT)

        return self._score
            
    def reset_score(self):
        self._score = 0
    
    def update_score(self):
        self._score += 1

    def get_score(self):
        return self._score
