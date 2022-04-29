import pygame

BLUE = (30, 144, 255)
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

