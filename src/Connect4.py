import numpy as np
from copy import deepcopy
from scipy.signal import convolve2d
import time



# Class that controls connect4 logic

class Connect4():
    # Constructor
    def __init__(self, width, height, in_a_row):
        # player 1 is 0
        # player 2 is 1
        # -1 is empty space
        self.width = width
        self.height = height
        self.in_a_row = in_a_row
        self.board = np.full((self.height, self.width), -1)
        #self.board = np.arange(42).reshape(self.height, self.width) #FIXME for debugging evals
        #self.check_winner(1)

    # Clears the board, (never used)
    def clear_board(self):
        self.board = np.full((self.height, self.width), -1)

    # Checks if position is open
    def is_open(self, pos):
        pos = pos-1
        return self.board[0][pos] == -1


    # Places piece into the board
    def place_piece(self, pos, player):
        pos = pos-1
        for row in range(self.height-1, -1, -1):    #starts at the bottom, goes to the top
            if self.board[row][pos] == -1:
                self.board[row][pos] = player
                return row
        return -1

    # evaluates the board
    def evaluate(self, player, heuristic):
        total = heuristic.evaluate(self.board, player)
        return total


   

    
    # Helper function for minimax
    def get_next_move(self, board, move, player):
        board2 = deepcopy(board)
        board2.place_piece(move, player)
        return board2

    # makes the board into nice looking board for CMD
    def print_map(self, x):
        if x == -1:
            return "."
        elif x == 0:
            return "A"
        else:
            return "B"

    # Prints the board
    def print_board(self):
        print()
        print(np.vectorize(self.print_map)(self.board))

    # Checks if the board has a winner
    def is_there_a_winner(self):
        if self.check_winner(0):
            return True
        if self.check_winner(1):
            return True
        if self.is_full():
            return True
        return False

    # Checks if a specific player has won
    def check_winner(self, player):
        

        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        for kernel in detection_kernels:
           
            if (convolve2d(self.board == player, kernel, mode="valid") == 4).any():
                
                return True
        return False

    #Checks if the board is full
    def is_full(self):
        for i in range(1, 7):
            if self.is_open(i):
                return False
        return True
                
        
