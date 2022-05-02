from Connect4 import Connect4
import pygame
import random
import time

from board import Board

WIDTH = 1050
HEIGHT = 800
SQUARE_SIZE = 133
FPS = 60

valid_inputs = [1, 2, 3, 4, 5, 6, 7]

def main():
    inp = input("Text(t) or pygame(p)?: ")
    if inp == "t":
        text_game_loop()
    else:
        pyGameLoop()

def text_game_loop():
    board = Connect4()
    board.print_board()
    pcount= 0

    inp = int(input("\nPlayer " + str(pcount%2) + ", Drop a piece (1-7): "))
    while not board.is_there_a_winner():
        if board.is_open(inp):
            board.place_piece(inp, pcount%2)
            board.print_board()

            p1, t1 = board.evaluate(0)
            p2, t2 = board.evaluate(1)
            p1k, t1k = board.evaluate_k(0)
            p2k, t2k = board.evaluate_k(1)

            print("V p1: " + str(p1) + " | V_K p1: " + str(p1k))
            print("V p2: " + str(p2) + " | V_K p2: " + str(p2k))
            print("Custom: [" + format(t1, ".2f") + "ms, " + format(t2, ".2f") + "ms]")
            print("Kernel: [" + format(t1k, ".2f") + "ms, " + format(t2k, ".2f") + "ms]")
            pcount += 1
        else:
            print("no space to drop")
        if not board.is_there_a_winner():
            inp = int(input("\nPlayer " + str(pcount % 2) + ", Drop a piece (1-7): "))
            while inp not in valid_inputs:
                inp = int(input("\nPlayer " + str(pcount%2) + ", Drop a piece (1-7): "))
            

def get_row_col_from_mouse(pos):
    x, y = pos
    col = (x - 66) // SQUARE_SIZE
    return col+1

def choose_game():
    return input("Press 1 for two player game, press 2 for player/random game.")


def pyGameLoop():
    choice = int(choose_game())
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect Four++")
    game = Connect4(WIN)
    clock = pygame.time.Clock()
    pygame.display.update()
    if choice == 1:
        two_player_loop(game, clock)
    elif choice == 2:
        player_random_loop(game, clock)
    

def two_player_loop(game, clock):
    run = True
    player = 0

    while run:
        clock.tick(FPS)
        pygame.display.update()
        if game.is_there_a_winner():
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  #
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = get_row_col_from_mouse(pos)
                if game.is_open(col):
                    game.place_piece(col, player)
                    player = (player + 1) % 2
                    print(col)
                else:
                    print("no space to drop")

def player_random_loop(game, clock):
    run = True
    player = 0

    while run:
        clock.tick(FPS)
        pygame.display.update()
        if game.is_there_a_winner() == True:
            run = False
        if player == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False #

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = get_row_col_from_mouse(pos)
                    if game.is_open(col):
                        game.place_piece(col, 0)
                        player = (player + 1) % 2
                        print(col)
                    else:
                        print("no space to drop")
        
        elif player == 1:
            time.sleep(1)
            col = random.randint(1, 7)
            while(not game.is_open(col)):
                col = random.randint(0, 6)

            game.place_piece(int(col) + 1, 1)
            player = (player + 1) % 2
            print(col)
            


if __name__ == '__main__':
    main()