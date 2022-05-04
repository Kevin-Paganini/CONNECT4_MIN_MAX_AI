import numpy as np
from copy import deepcopy
from scipy.signal import convolve2d
from board import Board
import time

from NullBoard import NullBoard


class Connect4():

    def __init__(self, win=None):
        # player 1 is 0
        # player 2 is 1
        # -1 is empty space
        self.width = 7
        self.height = 6
        self.in_a_row = 4
        self.board = np.full((self.height, self.width), -1)
        #self.board = np.arange(42).reshape(self.height, self.width) #FIXME for debugging evals
        self.check_winner(1)

    def is_open(self, pos):
        pos = pos-1
        return self.board[0][pos] == -1

    def place_piece(self, pos, player):
        pos = pos-1
        for row in range(self.height-1, -1, -1):    #starts at the bottom, goes to the top
            if self.board[row][pos] == -1:
                self.board[row][pos] = player
                return row
        return -1

    def evaluate(self, player):
        #print("\nEvals for player " + str(player) + ":")
        total = 0
        start = time.time()
        total += self.eval_columns(player)
        total += self.eval_rows(player)
        total += self.eval_left_diag(player)
        total += self.eval_right_diag(player)

        total -= self.eval_columns((player+1)%2)      #may need to add/remove this for minimax
        total -= self.eval_rows((player+1)%2)         #may need to add/remove this for minimax
        total -= self.eval_left_diag((player+1)%2)    #may need to add/remove this for minimax
        total -= self.eval_right_diag((player+1)%2)   #may need to add/remove this for minimax
        end = time.time()

        return total

    def eval_columns(self, player):
        total = 0
        for x in range(self.width):
            for y in range(self.height-(self.in_a_row-1)):
                col = [self.board[y+i][x] for i in range(self.in_a_row)]
                if (player+1)%2 not in col:
                    col = list(map(lambda a: 0 if a == -1 else 1, col))
                    total += self.get_sum(col)
        return total

    def eval_rows(self, player):
        total = 0
        for y in range(self.height):
            for x in range(self.width-(self.in_a_row-1)):
                row = self.board[y][x:x+self.in_a_row]
                if (player+1)%2 not in row:
                    row = list(map(lambda a: 0 if a == -1 else 1, row))
                    total += self.get_sum(row)
        return total

    def eval_left_diag(self, player):   #left diag = \
        total = 0
        for y in range(self.height-(self.in_a_row-1)):
            for x in range(self.width-(self.in_a_row-1)):
                ldiag = [self.board[y+i][x+i] for i in range(self.in_a_row)]
                if (player+1)%2 not in ldiag:
                    ldiag = list(map(lambda a: 0 if a == -1 else 1, ldiag))
                    total += self.get_sum(ldiag)
        return total

    def eval_right_diag(self, player):   #right diag = /
        total = 0
        for y in range(self.height-(self.in_a_row-1)):
            for x in range(self.in_a_row-1, self.width):
                rdiag = [self.board[y+i][x-i] for i in range(self.in_a_row)]
                if (player+1)%2 not in rdiag:
                    rdiag = list(map(lambda a: 0 if a == -1 else 1, rdiag))
                    total += self.get_sum(rdiag)
        return total

    def evaluate_k(self, player):
        total = 0
        start = time.time()

        board2 = deepcopy(self.board)               #this currently only works for the current player
        for i in range(self.height):                #still doesnt act as intended for .AAA. occurences
            for j in range(self.width):
                board2[i][j] = 0 if board2[i][j] != player else 1

        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        for kernel in detection_kernels:
            grad = convolve2d(self.board == player, kernel, mode="valid")
            #print(grad)
            if (grad == 2).any():
                total += 2
            if (grad == 3).any():
                total += 3
            if (grad == 4).any():
                total += 8
        end = time.time()
        return total

    def get_sum(self, group):
        s = sum(group)
        if s == self.in_a_row:  # double a 4 in a row, don't add singles (ex: [0, 0, 0, 1])
            #print("Group being added: " + str(group))
            return 10000000000000
        elif s >= 2:
            #print("Group being added: " + str(group))
            return s**3
        else:
            return 0

    def get_next_move(self, board, move, player):
        board2 = deepcopy(board)
        board2.place_piece(move, player)
        return board2


    def print_map(self, x):
        if x == -1:
            return "."
        elif x == 0:
            return "A"
        else:
            return "B"

    def print_board(self):
        print()
        print(np.vectorize(self.print_map)(self.board))


    def is_there_a_winner(self):
        if self.check_winner(0):
            return True
        if self.check_winner(1):
            return True
        return False

    def check_winner(self, player):
        # win_check_board = np.full((self.height, self.width), 0)
        # for row in self.board:
        #     for col in self.board:
        #         if (player == self.board[row][col]):
        #             win_check_board[row][col] = 1
        
        # print(win_check_board)

        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        for kernel in detection_kernels:
           
            if (convolve2d(self.board == player, kernel, mode="valid") == 4).any():
                
                return True
        return False
                
        
