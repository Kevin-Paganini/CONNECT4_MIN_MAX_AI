import sys
import time
import random
import pygame
import minimax
import csv

import numpy as np
from Pyboard import Pyboard
from Connect4 import Connect4
from CountingInARow import CountingInARow
from NeuralNetwork import NeuralNetwork

def main():
    pygame.init()
    pygame.display.set_caption("Connect Four++")
    game_board = Connect4(7, 6, 4)
    heur1 = CountingInARow(7, 6, 4)
    py_board = Pyboard(7, 6, game_board)
    clock = pygame.time.Clock()
    pygame.display.update()
    # Load in weights   
    x = load_weights()
    #print(x)
    NN = NeuralNetwork([42, 20, 7], x)
    p_loop(clock, py_board, heur1, NN)



def load_weights():
    np_load_old = np.load
    # modify the default parameters of np.load
    np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
    weights = 'size100_[42, 20, 7]_pop100_ep500_mut0.001_el5_fit0.57'
    with open(weights, 'rb') as f:
        ret = np.load(f)
    # restore np.load for future normal usage
    np.load = np_load_old
    return ret


# Pygame loop
def p_loop(clock, py_board, heur1, NN):
    players = ["Human", "Human"]
    button = 0
    player = 0
    winner = False
    start = False
    move_count = 0
    while button != -1:
        clock.tick(60)
        pygame.display.update()

        if players[player] == "Human" or not start or winner:
            button = int(listen(py_board))
        elif players[player] == "Random":
            button = 9      # random
        elif players[player] == "Minimax":
            button = 10     # minimax
        else:
            button = 30     # neural network

        if 14 < button < 23 and not start:    # set players
            if button == 15:
                players[0] = "Human"
            if button == 16:
                players[0] = "Minimax"
            if button == 17:
                players[0] = "Random"
            if button == 18:
                players[1] = "Human"
            if button == 19:
                players[1] = "Minimax"
            if button == 20:
                players[1] = "Random"
            if button == 21:
                players[0] = "Neural"
            if button == 22:
                players[1] = "Neural"
            py_board.refresh_side_buttons(players)


        if button == 12 and not start: #start
            py_board.refresh_midline_buttons([(200, 0, 0), (0, 200, 0)])
            py_board.display_info("It's your turn player 1. Place your piece!")
            start = True

        if start:

            depth = move_count//11 + 4
            if depth > 6:
                depth = 6

            if 0 < button < 8 and not winner:   # human
                if py_board.place_piece(button, player):
                    player = (player+1) % 2
                    move_count += 1
                    py_board.display_info("It's your turn player " + str(player+1) + ". Place your piece!")

            elif button == 9 and not winner: # random
                py_board.display_info("Random player " + str(player+1) + " is thinking...")
                time.sleep(0.2)
                col = random.randint(1, 7)
                while not py_board.is_open(col):
                    col = random.randint(1, 7)
                py_board.place_piece(col, player)
                player = (player + 1) % 2
                move_count += 1
                py_board.display_info("It's your turn player " + str(player) + ". Place your piece!")

            elif button == 10 and not winner: # minimax
                py_board.display_info("Minimax " + str(player+1) + " is thinking...")

                # depth = 2 this is for NN vs minimax demo
                val, pos = minimax.get_move(py_board.get_board(), depth, player, heur1)
                time.sleep(0.2)
                py_board.place_piece(pos, player)
                player = (player + 1) % 2
                move_count += 1
                py_board.display_info("It's your turn player " + str(player+1) + ". Place your piece!")

            elif button == 30 and not winner: # neural
                py_board.display_info("Neural Network " + str(player+1) + " is thinking...")
                f_board = py_board.get_board()
                f_board = f_board.board.flatten()
                out = NN.step(f_board)
                col = np.argmax(out) + 1
                if py_board.is_open(col):
                    time.sleep(0.2)
                    py_board.place_piece(col, player)
                else:
                    val, pos = minimax.get_move(py_board.get_board(), depth, player, heur1)
                    py_board.place_piece(pos, player)
                player = (player + 1) % 2
                move_count += 1
                py_board.display_info("It's your turn player " + str(player+1) + ". Place your piece!")

            elif button == 13:     # reset board
                py_board.clear_stuff(players)
                winner = False
                start = False
                player = 0
                move_count = 0

        if not winner and py_board.is_winner(players):
            winner = True


# Waiting for user input
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


#main
if __name__ == '__main__':
    main()