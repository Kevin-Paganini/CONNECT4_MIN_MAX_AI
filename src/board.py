import numpy
import pyautogui
import pygame
import os

WIDTH = 1050
HEIGHT = 1000

width = 800
height = 800

BLUE = (30, 144, 255)
BLACK = (0,0,0)
WHITE = (255,255,255)
PLAYER_0_COLOR = (51, 162, 29)
PLAYER_1_COLOR = (225, 34, 27)
EMPTY = (28, 26, 26)

class Board:

    def __init__(self, cols, rows):
        self.board = [[]]
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.rows = rows
        self.cols = cols
    
        self.create_board()


    def create_board(self):
        self.win.fill(BLUE)
        square_size = (1050 / self.cols) * 0.9
        for x in range(self.cols):
            for y in range(self.rows):
                pygame.draw.circle(self.win, EMPTY, (WIDTH/2 + (x*square_size/2 * (-1)**x) - x % 2*square_size/2, (y*square_size) + (square_size/2)), square_size/3)

                #pygame.draw.circle(self.win, EMPTY, (row * square_width, col * square_height), (square_width / 2 - 30))
        #for col in range(1, self.cols + 3):
            #pygame.draw.line(self.win, BLACK, ((col * square_width) - (square_width / 2), 0), ((col * square_width) - (square_width / 2), HEIGHT-100))


    def place_piece(self, row, pos, player):
        square_width = WIDTH / self.cols
        square_height = HEIGHT-100 / self.rows
        if player == 0:
            pygame.draw.circle(self.win, PLAYER_0_COLOR, (pos * square_width, (row+1) * square_height), (square_width / 2 - 15))
        else:
            pygame.draw.circle(self.win, PLAYER_1_COLOR, (pos * square_width, (row+1) * square_height), (square_width / 2 - 15))


    def display_win(self, player):
        pyautogui.confirm(player)


    def get_row_col_from_mouse(self, pos):
        x, y = pos
        col = (x - 66) // SQUARE_SIZE
        print(col + 1)
        return col + 1
