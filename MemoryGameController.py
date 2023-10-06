import time
import random
import utime
from Model import *
from Button import *
from Displays import *
from Lights import *
from SequenceGenerator import *
from PlayerInput import *

class MemoryGameController:
    def __init__(self):
        self._buttonW = Button(15, "Start Button", buttonhandler=None)
        self._buttonG = Button(16, "Green Button", buttonhandler=None)
        self._buttonR = Button(17, "Red Button", buttonhandler=None)
        self._buttonB = Button(18, "Blue Button", buttonhandler=None)
        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)
        self._dimlightG = DimLight(27, "Dim Light Green")
        self._dimlightR = DimLight(19, "Dim Light Red")
        self._dimlightB = DimLight(20, "Dim Light Blue")
        self.game_round = 0
        self.score = 0
        self.rounds_to_win = 3  # Number of rounds required to finish the game

        self._model = Model(4, self, debug=True)  # Updated to support 4 states

        self._model.addButton(self._buttonW)
        self._model.addButton(self._buttonG)
        self._model.addButton(self._buttonR)
        self._model.addButton(self._buttonB)

        # Define transitions
        self._model.addTransition(0, [BTN1_PRESS], 1)
        self._model.addTransition(1, [TIMEOUT], 2)
        self._model.addTransition(2, [TIMEOUT], 1)
        self._model.addTransition(2, [BTN1_PRESS], 3)
        self._model.addTransition(3, [BTN1_PRESS], 0)
        
        self.sequence_generator = SequenceGenerator(self._dimlightG, self._dimlightR, self._dimlightB)
        self.player_input = PlayerInput(self.sequence_generator, self._buttonG, self._buttonR, self._buttonB, self._model, self._display, self.score)


    def run(self):
        self._model.run()

    def stateEntered(self, state, event):
        if state == 0:
            self.score = 0
            self.game_round = 0
            self._display.reset()
            self._display.showText('Welcome to the Memory Game!')
        elif state == 1:
            self.game_round += 1
            score = self.player_input.get_score()
            self._display.reset()
            self._display.showText(f'Round {self.game_round}:')
            time.sleep(4)
            self._display.reset()
            self._display.showText(f'Current Score: {score}')
            time.sleep(4)
            self._display.reset()
            self._display.showText('Watch the sequence:')
            self.sequence_generator.generate_sequence()            
        elif state == 2:
            self._display.reset()
            self._display.showText('Repeat the sequence:')
        elif state == 3:
            score = self.player_input.get_score()
            self._display.reset()
            self._display.showText('Congratulations!')
            time.sleep(1)
            self._display.reset()
            self._display.showText(f'You won with a score of {score}!')
            time.sleep(4)
            self._display.reset()
            self._display.showText('Press the Start Button')
            time.sleep(1)
            self._display.reset()
            self._display.showText('To Play Again')


    def stateDo(self, state):
        if state == 0:
            self.player_input.reset_score()  # Reset the score at the beginning of each game
        elif state == 1:
            if not self.sequence_generator._sequence_displayed:
                current_time = utime.ticks_ms()
                if current_time - self.sequence_generator._sequence_start_time >= self.sequence_generator._sequence_display_time:
                    self.sequence_generator._sequence_displayed = True
                    self._model.processEvent(TIMEOUT)  # Transition to state 2 with BTN1_PRESS
        elif state == 2:
            print('Input Player Sequence....')
            if self.sequence_generator._sequence_displayed:
                self.player_input.player_input()
                
                # Check if the player has won enough rounds to transition to state 3
                if self.game_round > self.rounds_to_win:
                    self._model.processEvent(BTN1_PRESS)  # Transition to state 3 with BTN1_PRESS

        elif state == 3:
            pass

    def stateLeft(self, state, event):
        if state == 1:
            self._dimlightG.off()
        elif state == 2:
            self._dimlightR.off()



