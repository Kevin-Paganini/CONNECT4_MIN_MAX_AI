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
YELLOW = (200, 200, 0)
PLAYER_0_COLOR = (51, 162, 29)
PLAYER_1_COLOR = (200, 34, 27)
EMPTY = (28, 26, 26)

PLAYER_B_X_BUFF = 70
PLAYER1_B_Y = 850
PLAYER2_B_Y = 910
PLAYER_BUTTON_WIDTH = 90
P_B_PADDING = 5

poss_players = ["p", "m", "r", "n"]
p1_color = [GREEN, WHITE, WHITE]
p2_color = [GREEN, WHITE, WHITE]
FONT = 'freesansbold.ttf'
#FONT = "C:\Windows\Fonts\Arial.ttf"


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
        self.players = ["p", "p"]
        self.p1_color = [WHITE, WHITE, WHITE]#, WHITE]
        self.p2_color = [WHITE, WHITE, WHITE]#, WHITE]

        self.create_board()

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
        self.display_info("Hit start to start the game, or pick the players!")

        self.set_up_buttons(self.players)

    def set_up_buttons(self, players):   #pygame.Rect((left, top), (width, height)
        x = WIDTH / 2
        self.init_side_button("Start", x, GREEN, 40)   #490, 850 | 560, 890
        self.init_side_button("Reset", x, RED, 90)     #490, 900 | 560, 940
        self.init_side_button("Quit", x, WHITE, 140)     #490, 900 | 560, 940

        self.refresh_side_buttons(players)

    """
    def refresh_side_buttons2(self, players):
        self.p1_color = [WHITE, WHITE, WHITE, WHITE]
        self.p2_color = [WHITE, WHITE, WHITE, WHITE]
        idx1 = poss_players.index(players[0])
        idx2 = poss_players.index(players[1])
        self.p1_color[idx1] = GREEN
        self.p2_color[idx2] = GREEN



    def init_side_button2(self):
    """


    def refresh_side_buttons(self, players):
        self.p1_color = [WHITE, WHITE, WHITE]
        self.p2_color = [WHITE, WHITE, WHITE]
        idx1 = poss_players.index(players[0])
        idx2 = poss_players.index(players[1])
        self.p1_color[idx1] = GREEN
        self.p2_color[idx2] = GREEN

        x = 70
        self.init_side_button("Player 1", x, BLACK, 0)
        self.init_side_button("Human", x, self.p1_color[0], 45)  # 25, 860 | 115, 895
        self.init_side_button("Minimax", x, self.p1_color[1], 90)  # 20, 900 | 120, 940
        self.init_side_button("Random", x, self.p1_color[2], 135)  # 20, 950 | 120, 990

        x = 200
        self.init_side_button("Player 2", x, BLACK, 0)
        self.init_side_button("Human", x, self.p2_color[0], 45)  # 155 860 | 245, 895
        self.init_side_button("Minimax", x, self.p2_color[1], 90)  # 150 900 | 250, 940
        self.init_side_button("Random", x, self.p2_color[2], 135)  # 150 950 | 250, 990

    def init_midline_button(self, text, color, buffer):
        self.init_side_button(text, WIDTH/2, color, buffer)

    def init_side_button(self, text, x, color, buffer):
        font = pygame.font.Font(FONT, 20)
        text = font.render(text, True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (x, self.bottom_of_board + 25 + buffer)
        color_rect = pygame.Rect((text_rect.left - 10, text_rect.top - 10), (text_rect.width + 20, text_rect.height + 20))
        white_rect = pygame.Rect((text_rect.left - 5, text_rect.top - 5), (text_rect.width + 10, text_rect.height + 10))
        print(text_rect.width)
        pygame.draw.rect(self.win, color, color_rect)
        pygame.draw.rect(self.win, WHITE, white_rect)
        self.win.blit(text, text_rect)

    def is_open(self, col):
        return self.board.is_open(col)

    def place_piece(self, col, player):
        if self.board.is_open(col):
            row = self.board.place_piece(col, player)
            if player == 0:
                pygame.draw.circle(self.win, PLAYER_0_COLOR, (self.buff + (col - 1) * self.square_size + self.square_size / 2, row * self.square_size + self.square_size / 2), self.square_size / 3)
            else:
                pygame.draw.circle(self.win, PLAYER_1_COLOR, (self.buff + (col - 1) * self.square_size + self.square_size / 2, row * self.square_size + self.square_size / 2), self.square_size / 3)
            self.display_info("It's your turn player " + str((player+1)%2 + 1) + ". Place your piece!")
            return True
        return False

    def get_row_col_from_mouse(self, mouse):
        col = (mouse[0] - (self.square_size/2) + 15) // self.square_size + 1
        if col > 7 or col < 1:
            return 0
        else:
            return int(col)

    def get_button_from_mouse(self, mouse):
        x = mouse[0]
        y = mouse[1]
        if 490 < x < 560 and 850 < y < 890:
            return 12 # start button
        if 490 < x < 560 and 900 < y < 940:
            return 13 # reset button
        if 490 < x < 560 and 950 < y < 990:
            pygame.quit()
            sys.exit()
        if 25 < x < 115 and 860 < y < 895:
            return 15 # human p1
        if 20 < x < 120 and 900 < y < 940:
            return 16 # minimax p1
        if 20 < x < 120 and 950 < y < 990:
            return 17 # random p1
        if 155 < x < 245 and 860 < y < 895:
            return 18  # human p2
        if 150 < x < 250 and 900 < y < 940:
            return 19  # minimax p2
        if 150 < x < 250 and 950 < y < 990:
            return 20  # random p2
        return 0

    def clear_p1_buttons(self):
        x = 70
        self.init_side_button("Human", x, WHITE, 45)  # 25, 860 | 115, 895
        self.init_side_button("Minimax", x, WHITE, 90)  # 20, 900 | 120, 940
        self.init_side_button("Random", x, WHITE, 135)  # 20, 950 | 120, 990

    def clear_p2_buttons(self):
        x = 200
        self.init_side_button("Human", x, WHITE, 45)  # 155 860 | 245, 895
        self.init_side_button("Minimax", x, WHITE, 90)  # 150 900 | 250, 940
        self.init_side_button("Random", x, WHITE, 135)  # 150 950 | 250, 990

    def update_mouse_pos(self, mouse):
        self.display_mouse(mouse)
        self.show_col_highlight(mouse)

    def show_col_highlight(self, mouse):
        col = self.get_row_col_from_mouse(mouse)
        if self.curr_col != col and 0 < col < 8 and self.board.is_open(col):
            self.clear_col_highlight()
            pygame.draw.circle(self.win, (255,255,0), (self.buff + (col-1) * self.square_size + self.square_size/2, self.square_size/2), self.square_size/3)
            pygame.draw.circle(self.win, EMPTY, (self.buff + (col-1) * self.square_size + self.square_size / 2, self.square_size / 2),self.square_size / 3.5)
            self.curr_col = col

    def clear_col_highlight(self):
        for x in range(self.cols):
            if self.board.is_open(x+1):
                pygame.draw.circle(self.win, EMPTY,(self.buff + x * self.square_size + self.square_size / 2, self.square_size / 2), self.square_size / 3)

    def display_mouse(self, mouse):
        inf = str(mouse[0]) + ", " + str(mouse[1])
        font = pygame.font.Font(FONT, 20)
        text = font.render(inf, True, BLACK, YELLOW)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH-text_rect.width + 20, HEIGHT - 20)
        back = pygame.Rect((text_rect.left-30, text_rect.top-10), (text_rect.width + 60, text_rect.height + 20))
        pygame.draw.rect(self.win, YELLOW, back)
        self.win.blit(text, text_rect)

    def is_winner(self):
        if self.board.check_winner(0):
            self.display_info("Player 1 is the winner!")
            return True
        elif self.board.check_winner(1):
            self.display_info("Player 2 is the winner!")
            return True
        elif self.board.is_full():
            self.display_info("It's a draw!")
            return True
        else:
            return False

    def display_info(self, info):
        font = pygame.font.Font(FONT, 20)
        text = font.render(info, True, BLACK, YELLOW)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH/2, self.bottom_of_board + 15)
        pygame.draw.rect(self.win, YELLOW, pygame.Rect((text_rect.centerx-250, text_rect.top - 5), (500, text_rect.height + 10)))
        self.win.blit(text, text_rect)

    def display_info2(self, info):
        self.display_info(info)

    def clear_stuff(self, players):
        self.board.clear_board()
        self.create_board()
        self.refresh_side_buttons(players)

    def get_board(self):
        return self.board

    def upd_players(self, p):
        self.players = p
