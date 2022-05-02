import pygame
import os

BLUE = (30, 144, 255)
BLACK = (0,0,0)
PLAYER_0_COLOR = (51, 162, 29)
PLAYER_1_COLOR = (225, 34, 27)
EMPTY = (28, 26, 26)
width = 800
height = 800

class Board:

    def __init__(self, WIN, rows, cols):
        self.board = [[]]
        self.win = WIN
        self.rows = rows
        self.cols = cols
    
        self.create_board()


    def create_board(self):
        self.win.fill(BLUE)
        square_width = (width) / self.cols
        square_height = (height) / self.rows
        for col in range(1, self.cols + 1):
            for row in range(1, self.rows + 1):
                pygame.draw.circle(self.win, EMPTY, (row * square_width, col * square_height), (square_width / 2 - 15))
        for col in range(1, self.cols + 3):
            pygame.draw.line(self.win, BLACK, ((col * square_width) - (square_width / 2), 0), ((col * square_width) - (square_width / 2), 800))
            
            

    def place_piece(self, pos, player):
        pos = pos-1
        ret = 0
        for row in range(self.height-1, -1, -1):    #starts at the bottom, goes to the top
            if self.board[row][pos] == -1:
                ret = row
                break
                
        
        square_width = (width) / self.cols
        square_height = (height) / self.rows
        if player == 0:
            pygame.draw.circle(self.win, PLAYER_0_COLOR, (pos * square_width, ret * square_height), (square_width / 2 - 15))
        else:
            pygame.draw.circle(self.win, PLAYER_1_COLOR, (pos * square_width, ret * square_height), (square_width / 2 - 15))

