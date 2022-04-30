from Connect4 import Connect4
import pygame
import random
import time


WIDTH = 1050
HEIGHT = 800
SQUARE_SIZE = 133

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("Connect Four++")

valid_inputs = ['1', '2', '3', '4', '5', '6', '7']

def main():
    #text_game_loop()
    pyGameLoop()

def text_game_loop():
    board = Connect4()
    board.print_board()
    pcount= 0

    inp = int(input("\nPlayer " + str(pcount%2) + ", Drop a piece (1-7): "))
    Flag = True
    while(not board.is_there_a_winner()):
        if(board.is_open(inp)):
            board.place_piece(int(inp), pcount%2)
            board.print_board()
            print("Value for player " + str(pcount%2 + 1) + ": " + str(board.evaluate(pcount%2)))
            
            print("Value for player " + str((pcount+1) % 2 + 1) + ": " + str(board.evaluate((pcount+1) % 2)))
            
            pcount += 1
        else:
            print("no space to drop")
        if not board.is_there_a_winner():
            while(input("\nPlayer " + str(pcount%2) + ", Drop a piece (1-7): ") not in valid_inputs):
                input("\nPlayer " + str(pcount%2) + ", Drop a piece (1-7): ")
            

def get_row_col_from_mouse(pos):
    x, y = pos
    col = (x - 66) // SQUARE_SIZE
    return col

def choose_game():
    return input("Press 1 for two player game, press 2 for player/random game.")


def pyGameLoop():
    choice = int(choose_game())
    game = Connect4(WIN)
    clock = pygame.time.Clock()
    pygame.display.update()
    if choice == 1:
        two_player_loop(game, clock)
    elif choice == 2:
        player_random_loop(game, clock)
    

def two_player_loop(game, clock):
    run = True

    while run:
        clock.tick(FPS)
        pygame.display.update()
        if game.is_there_a_winner() == True:
            run = False
        if game.turn == 0:
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False #

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col  = get_row_col_from_mouse(pos)
                    if(game.is_open(col)):
                        game.place_piece(int(col) + 1, 0)
                        print(col)
                    else:
                        print("no space to drop")
        
        elif game.turn == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False #

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col  = get_row_col_from_mouse(pos)
                    if(game.is_open(col)):
                        game.place_piece(int(col) + 1, 1)

                        print(col)

                    else:
                        print("no space to drop")

def player_random_loop(game, clock):
    run = True

    while run:
        clock.tick(FPS)
        pygame.display.update()
        if game.is_there_a_winner() == True:
            run = False
        if game.turn == 0:
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False #

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col  = get_row_col_from_mouse(pos)
                    if(game.is_open(col)):
                        game.place_piece(int(col) + 1, 0)
                        print(col)
                    else:
                        print("no space to drop")
        
        elif game.turn == 1:
            time.sleep(1)
            col = random.randint(0, 6)
            while(not game.is_open(col)):
                col = random.randint(0, 6)

            game.place_piece(int(col) + 1, 1)

            print(col)

            


if __name__ == '__main__':
    main()