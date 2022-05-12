import sys
import pygame

WIDTH = 1050
HEIGHT = 1000

width = 800
height = 800

BLUE = (30, 144, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (100, 100, 100)
PLAYER_1_COLOR = (200, 200, 29)
PLAYER_0_COLOR = (200, 34, 27)
EMPTY = (28, 26, 26)

PLAYER_B_X_BUFF = 20
PLAYER1_B_Y = 880
PLAYER2_B_Y = PLAYER1_B_Y + 60
PLAYER_BUTTON_WIDTH = 90
P_B_PADDING = 5
P_B_SPACING = 10

poss_players = ["Human", "Minimax", "Neural", "Random"]
FONT = 'freesansbold.ttf'
#FONT = "C:\Windows\Fonts\Arial.ttf"

###################################################
# Handles all of GUI elements
###################################################

class Pyboard:

    def __init__(self, cols, rows, board):
        self.board = board
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.rows = rows
        self.cols = cols
        self.square_size = (1050 / self.cols) * 0.9
        self.curr_col = 0
        self.buff = 52.5
        self.bottom_of_board = HEIGHT - (HEIGHT - self.square_size*6)-2
        self.players = ["Human", "Human"]
        self.p1_color = [WHITE, WHITE, WHITE, WHITE]
        self.p2_color = [WHITE, WHITE, WHITE, WHITE]

        self.create_board()

    # Creates the board
    def create_board(self):
        self.win.fill(BLUE)
        pygame.draw.rect(self.win, YELLOW, pygame.Rect((0, 0), (self.buff, HEIGHT)))
        pygame.draw.rect(self.win, YELLOW, pygame.Rect((WIDTH-self.buff, 0), (WIDTH-self.buff, HEIGHT)))

        for x in range(self.cols):
            for y in range(self.rows):
                pygame.draw.circle(self.win, EMPTY, (self.buff + x*self.square_size + self.square_size/2, y*self.square_size + self.square_size/2), self.square_size/3)
            pygame.draw.line(self.win, BLACK, (self.buff + (x+1)*self.square_size, 0), (self.buff + (x+1)*self.square_size, self.bottom_of_board))

        pygame.draw.line(self.win, BLACK, (self.buff, 0), (self.buff, self.bottom_of_board))
        pygame.draw.rect(self.win, YELLOW, pygame.Rect((0, self.bottom_of_board), (WIDTH, HEIGHT-self.bottom_of_board)))
        pygame.draw.line(self.win, BLACK, (self.buff, self.bottom_of_board-1), (WIDTH-self.buff, self.bottom_of_board-1))

        self.set_up_buttons(self.players)
        self.display_info("Hit start to start the game, or pick the players!")

    # Sets up the buttons
    def set_up_buttons(self, players):   #pygame.Rect((left, top), (width, height)
        self.refresh_midline_buttons([GREEN, RED])
        self.refresh_side_buttons(players)

    def refresh_midline_buttons(self, colors):
        x = WIDTH/2 + 110
        y = self.bottom_of_board + 10
        buff = 45
        self.init_side_button2(x, "Start", colors[0], y+buff)
        self.init_side_button2(x, "Reset", colors[1], y+buff*2)
        self.init_side_button2(x, "Quit", WHITE, y+buff*3)


    def refresh_side_buttons(self, players):
        self.p1_color = [WHITE, WHITE, WHITE, WHITE]
        self.p2_color = [WHITE, WHITE, WHITE, WHITE]
        idx1 = poss_players.index(players[0])
        idx2 = poss_players.index(players[1])
        self.p1_color[idx1] = GREEN
        self.p2_color[idx2] = GREEN

        c_r_right = self.init_side_button2(PLAYER_B_X_BUFF, "Player 1", BLACK, PLAYER1_B_Y)
        c_r_right = self.init_side_button2(P_B_SPACING + c_r_right + P_B_PADDING, "Human", self.p1_color[0], PLAYER1_B_Y)
        c_r_right = self.init_side_button2(P_B_SPACING + c_r_right + P_B_PADDING, "Minimax", self.p1_color[1], PLAYER1_B_Y)
        c_r_right = self.init_side_button2(P_B_SPACING + c_r_right + P_B_PADDING, "Neural", self.p1_color[2], PLAYER1_B_Y)
        self.init_side_button2(P_B_SPACING + c_r_right + P_B_PADDING, "Random", self.p1_color[3], PLAYER1_B_Y)

        c_r_right = self.init_side_button2(PLAYER_B_X_BUFF, "Player 2", BLACK, PLAYER2_B_Y)
        c_r_right = self.init_side_button2(P_B_SPACING + c_r_right + P_B_PADDING, "Human", self.p2_color[0],PLAYER2_B_Y)
        c_r_right = self.init_side_button2(P_B_SPACING + c_r_right + P_B_PADDING, "Minimax", self.p2_color[1], PLAYER2_B_Y)
        c_r_right = self.init_side_button2(P_B_SPACING + c_r_right + P_B_PADDING, "Neural", self.p2_color[2],PLAYER2_B_Y)
        self.init_side_button2(P_B_SPACING + c_r_right + P_B_PADDING, "Random", self.p2_color[3], PLAYER2_B_Y)


    def init_side_button2(self, x_pos, string, color, y):
        pad = P_B_PADDING
        font = pygame.font.Font(FONT, 20)
        text = font.render(string, True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (x_pos + PLAYER_BUTTON_WIDTH/2, y)
        color_rect = pygame.Rect((text_rect.left - pad*2, text_rect.top - pad*2), (PLAYER_BUTTON_WIDTH + pad*4, text_rect.height + pad*4))
        color_rect.center = text_rect.center
        white_rect = pygame.Rect((text_rect.left - pad, text_rect.top - pad), (PLAYER_BUTTON_WIDTH + pad*2, text_rect.height + pad*2))
        white_rect.center = text_rect.center
        pygame.draw.rect(self.win, color, color_rect)
        pygame.draw.rect(self.win, WHITE, white_rect)
        self.win.blit(text, text_rect)
        #print(str(string) + ": " + str(color_rect.left - 10) + " < x < " + str(color_rect.right + 10) + " and " + str(color_rect.top - 5) + " < y < " + str(color_rect.bottom + 5) + ":")
        return color_rect.right

    # Checks if board is open
    def is_open(self, col):
        return self.board.is_open(col)

    # Places piece to board
    def place_piece(self, col, player):
        if self.board.is_open(col):
            row = self.board.place_piece(col, player)
            if player == 0:
                pygame.draw.circle(self.win, PLAYER_0_COLOR, (self.buff + (col - 1) * self.square_size + self.square_size / 2, row * self.square_size + self.square_size / 2), self.square_size / 3)
            else:
                pygame.draw.circle(self.win, PLAYER_1_COLOR, (self.buff + (col - 1) * self.square_size + self.square_size / 2, row * self.square_size + self.square_size / 2), self.square_size / 3)
            return True
        return False

    # Gets row and col from mouse
    # Really only need col 
    def get_row_col_from_mouse(self, mouse):
        col = (mouse[0] - (self.square_size/2) + 15) // self.square_size + 1
        if col > 7 or col < 1:
            return 0
        else:
            return int(col)

    # Gets what button wqas clicked from mouse
    def get_button_from_mouse(self, mouse):
        x = mouse[0]
        y = mouse[1]
        if 615 < x < 745 and 838 < y < 888:
            return 12 # start button
        if 615 < x < 745 and 883 < y < 933:
            return 13 # reset button
        if 615 < x < 745 and 928 < y < 978:
            pygame.quit()
            sys.exit()
        if 115 < x < 245 and 855 < y < 905:
            return 15 # human p1
        if 230 < x < 360 and 855 < y < 905:
            return 16 # minimax p1
        if 345 < x < 475 and 855 < y < 905:
            return 21 # nearual net p1
        if 460 < x < 590 and 855 < y < 905:
            return 17 # random p1
        if 115 < x < 245 and 915 < y < 965:
            return 18  # human p2
        if 230 < x < 360 and 915 < y < 965:
            return 19  # minimax p2
        if 345 < x < 475 and 915 < y < 965:
            return 22 # neural net p2
        if 460 < x < 590 and 915 < y < 965:
            return 20  # random p2
        return 0

    # Updates mouse position and highlights column
    def update_mouse_pos(self, mouse):
        self.display_mouse(mouse)
        self.show_col_highlight(mouse)

    # Highlights sepcific column
    def show_col_highlight(self, mouse):
        col = self.get_row_col_from_mouse(mouse)
        if self.curr_col != col and 0 < col < 8 and self.board.is_open(col):
            self.clear_col_highlight()
            pygame.draw.circle(self.win, (0,255,0), (self.buff + (col-1) * self.square_size + self.square_size/2, self.square_size/2), self.square_size/3)
            pygame.draw.circle(self.win, EMPTY, (self.buff + (col-1) * self.square_size + self.square_size / 2, self.square_size / 2),self.square_size / 3.5)
            self.curr_col = col

    # Clears column highlight
    def clear_col_highlight(self):
        for x in range(self.cols):
            if self.board.is_open(x+1):
                pygame.draw.circle(self.win, EMPTY,(self.buff + x * self.square_size + self.square_size / 2, self.square_size / 2), self.square_size / 3)

    # Displays where mouse is
    def display_mouse(self, mouse):
        inf = str(mouse[0]) + ", " + str(mouse[1])
        font = pygame.font.Font(FONT, 20)
        text = font.render(inf, True, BLACK, YELLOW)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH-text_rect.width + 20, HEIGHT - 20)
        back = pygame.Rect((text_rect.left-30, text_rect.top-10), (text_rect.width + 60, text_rect.height + 20))
        pygame.draw.rect(self.win, YELLOW, back)
        self.win.blit(text, text_rect)

    # Checks board and sees if there is a winner
    def is_winner(self, players):
        if self.board.check_winner(0):
            self.display_info("Player 1 (" + players[0] + ") is the winner!")
            return True
        elif self.board.check_winner(1):
            self.display_info("Player 2 (" + players[1] + ") is the winner!")
            return True
        elif self.board.is_full():
            self.display_info("It's a draw!")
            return True
        else:
            return False

    # Display info for board
    def display_info(self, info):
        font = pygame.font.Font(FONT, 20)
        text = font.render(info, True, BLACK, YELLOW)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH/2, self.bottom_of_board + 15)
        pygame.draw.rect(self.win, YELLOW, pygame.Rect((text_rect.centerx-250, text_rect.top - 5), (500, text_rect.height + 10)))
        self.win.blit(text, text_rect)
        pygame.display.update()

    # Clears board
    def clear_stuff(self, players):
        self.board.clear_board()
        self.create_board()
        self.refresh_side_buttons(players)

    # Gets connect 4 board
    def get_board(self):
        return self.board

    # Updates players being used
    def upd_players(self, p):
        self.players = p
