import numpy as np

class Connect4():

    def __init__(self):
        self._board = np.zeros((6, 7))

    def is_open(self, pos):
        pos = pos-1
        return self._board[0][pos] == 0

    def place_piece(self, pos, player):
        pos = pos-1
        for row in range(5, -1, -1):
            if self._board[row][pos] == 0:
                self._board[row][pos] = player
                return row



    def print_board(self):
        print(self._board)
