import sys
import time
import random
import pygame
import minimax

from Pyboard import Pyboard
from Connect4 import Connect4
from CountingInARow import CountingInARow


def main():
    pygame.init()
    pygame.display.set_caption("Connect Four++")
    game_board = Connect4(7, 6, 4)
    heur1 = CountingInARow(7, 6, 4)
    py_board = Pyboard(7, 6, game_board)
    clock = pygame.time.Clock()
    pygame.display.update()

    p_loop(clock, py_board, heur1)


def p_loop(clock, py_board, heur1):
    players = ["p", "p"]
    button = 0
    player = 0
    winner = False
    start = False
    while button != -1:
        clock.tick(60)
        pygame.display.update()

        if players[player] == "p" or not start or winner:
            button = int(listen(py_board))
        elif players[player] == "r":
            button = 9      # random
        else:
            button = 10     # minimax

        if 14 < button < 21 and not start:    # set players
            if button == 15:
                py_board.clear_p1_buttons()
                py_board.init_left_button("Human", (0, 200, 0), 45)
                players[0] = "p"
            if button == 16:
                py_board.clear_p1_buttons()
                py_board.init_left_button("Minimax", (0, 200, 0), 90)
                players[0] = "m"
            if button == 17:
                py_board.clear_p1_buttons()
                py_board.init_left_button("Random", (0, 200, 0), 135)
                players[0] = "r"
            if button == 18:
                py_board.clear_p2_buttons()
                py_board.init_right_button("Human", (0, 200, 0), 45)
                players[1] = "p"
            if button == 19:
                py_board.clear_p2_buttons()
                py_board.init_right_button("Minimax", (0, 200, 0), 90)
                players[1] = "m"
            if button == 20:
                py_board.clear_p2_buttons()
                py_board.init_right_button("Random", (0, 200, 0), 135)
                players[1] = "r"

        if button == 12 and not start: #start
            py_board.init_midline_button("Start", (200, 0, 0), 40)
            py_board.init_midline_button("Reset", (0, 200, 0), 90)
            py_board.display_info("It's your turn player 1. Place your piece!")
            start = True

        if start:
            if 0 < button < 8 and not winner:   # human
                if py_board.place_piece(button, player):
                    player = (player+1) % 2

            elif button == 9 and not winner: # random
                py_board.display_info2("Random player is thinking...")  # for some reason this isn't displaying?
                time.sleep(0.2)
                col = random.randint(1, 7)
                while not py_board.is_open(col):
                    col = random.randint(1, 7)
                py_board.place_piece(col, player)
                player = (player + 1) % 2

            elif button == 10 and not winner: # minimax
                py_board.display_info2("Minimax is thinking...")    # for some reason this isn't displaying?
                val, pos = minimax.get_move(py_board.get_board(), 4, player, heur1)
                py_board.place_piece(pos, player)
                player = (player + 1) % 2

            elif button == 13:     # reset board
                py_board.clear_stuff(players)
                winner = False
                start = False
                player = 0

        if not winner and py_board.is_winner():
            winner = True

def listen(py_board):
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[1] > 800:
                return py_board.get_button_from_mouse(mouse)
            else:
                return py_board.get_row_col_from_mouse(mouse)

    py_board.update_mouse_pos(mouse)
    return 0

if __name__ == '__main__':
    main()