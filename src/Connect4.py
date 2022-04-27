import numpy as np

class Connect4():

    def __init__(self):
        self._board = np.zeros((6, 7))

    def print_board(self):
        print(self._board)
