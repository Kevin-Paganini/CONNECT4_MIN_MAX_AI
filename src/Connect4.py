import numpy as np
from copy import deepcopy

class Connect4():

    def __init__(self):
        self._board = np.full((6, 7), -1)

    def is_open(self, pos):
        pos = pos-1
        return self._board[0][pos] == -1

    def place_piece(self, pos, player):
        pos = pos-1
        for row in range(5, -1, -1):
            if self._board[row][pos] == -1:
                self._board[row][pos] = player
                return row
        return -1

    def evaluate(self, player):
        total = 0
        total += self.eval_columns(player)
        total -= self.eval_columns((player+1)%2)    #may need to remove this for minimax
        #total += self.eval_rows(board, player)
        #total += self.eval_diagonals(board, player)
        return total

    def eval_columns(self, player):
        total = 0
        for y in range(7):      #no need to check above x,y piece, only below
            for x in range(3):
                col = [self._board[i][y] for i in range(x, x+4 if x < 3 else 6)]    #[-1, 0, 1, 1]
                if (player+1)%2 not in col: #if opposite player is in the column, don't consider
                    col = list(map(lambda a: 0 if a == player + 1 % 2 or a == -1 else 1, col))
                    s = sum(col)  #maps all non player symbols to 0
                    if s == 4:      #double a 4 in a row, don't add single pieces
                        total += 8
                    elif s >= 2:
                        total += s
        return total





    def get_next_moves(self, board, player):
        next = []
        for i in range(7):
            board2 = deepcopy(board)
            move = board2.place_piece(i+1, player)
            if move != -1:
                next.append(board2)
        return next


    def print_map(self, x):
        if x == -1:
            return "."
        elif x == 0:
            return "A"
        else:
            return "B"

    def print_board(self):
        print()
        print(np.vectorize(self.print_map)(self._board))
