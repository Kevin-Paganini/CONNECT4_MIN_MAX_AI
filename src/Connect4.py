import numpy as np
from copy import deepcopy
from scipy.signal import convolve2d
from board import Board



class Connect4():

    def __init__(self, win):
        # player 1 is 0
        # player 2 is 1
        # -1 is empty space
        self.width = 7
        self.height = 6
        self.board = np.full((self.height, self.width), -1)
        self.check_winner(1)
        self.win = win
        self.turn = 0
        self.board_py_game = Board(win, self.width, self.height)

    def is_open(self, pos):
        pos = pos-1
        return self.board[0][pos] == -1

    def place_piece(self, pos, player):
        pos = pos-1
        for row in range(self.height-1, -1, -1):    #starts at the bottom, goes to the top
            if self.board[row][pos] == -1:
                self.board[row][pos] = player
                self.board_py_game.place_piece(row + 1, pos + 1, self.turn)
                if self.turn == 0:
                    self.turn = 1
                else:
                    self.turn = 0
                return row
        return -1

    def evaluate(self, player):
        total = 0
        total += self.eval_columns(player)
        #total -= self.eval_columns((player+1)%2)    #may need to add/remove this for minimax
        total += self.eval_rows(player)
        #total += self.eval_diagonals(board, player)
        return total

    def eval_columns(self, player):
        total = 0
        for x in range(self.width):      #no need to check above x,y piece, only below
            for y in range(self.height-3):
                col = [self.board[i][x] for i in range(y, y + 4 if y < 3 else self.height)]    #ex of col: [-1, 0, 1, 1]
                if (player+1)%2 not in col: #if opposite player is in the column, don't consider
                    col = list(map(lambda a: 0 if a == -1 else 1, col)) #maps empty to 0
                    s = sum(col)
                    if s == 4:      #double a 4 in a row, don't add singles (ex: [0, 0, 0, 1])
                        total += 8
                    elif s >= 2:
                        total += s
        return total

    def eval_rows(self, player):
        total = 0
        for y in range(self.height):
            for x in range(self.width-3):
                row = self.board[y][x:x+4]
                if (player+1)%2 not in row:
                    row = list(map(lambda a: 0 if a == -1 else 1, row))
                    s = sum(row)
                    if s == 4:  # double a 4 in a row, don't add singles (ex: [0, 0, 0, 1])
                        total += 8
                    elif s >= 2:
                        total += s
        return total


    def get_next_moves(self, board, player):
        next = []
        for i in range(self.width):
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
        horizontal_kernel = np.array([[ 1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        for kernel in detection_kernels:
            if (convolve2d(self.board == player, kernel, mode="valid") == 4).any():
                return True
        return False
                
        
