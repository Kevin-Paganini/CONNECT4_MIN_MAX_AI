from Connect4 import Connect4
import pygame
import random
import time
import minimax

from board import Board
import minimax

WIDTH = 1050
HEIGHT = 800
SQUARE_SIZE = 133
FPS = 60

valid_inputs = [1, 2, 3, 4, 5, 6, 7]
players = ["p", "p"]


def main():
    while True:
        inp = input("Text(t), pygame(p), setPlayers(s), quit(q)?: ")
        if inp == "t":
            text_game_loop2()
        elif inp == "p":
            pyGameLoop()

        elif inp == "s":
            setPlayers()
        
        elif inp == "q":
            break
        


def setPlayers():
    player1choice = input("Plese enter player one choice (m for minimax, p for player, r for random)")
    player2choice = input("Plese enter player two choice (m for minimax, p for player, r for random)")
    players.clear()
    players.append(player1choice)
    players.append(player2choice)


def text_game_loop2():
    board = Connect4()
    board.print_board()
    player = 0

    while not board.is_there_a_winner():
        board.print_board()
        print(f'Player: {player}')
        if players[player] == "p":
            get_player_move(player, board)
                
        elif players[player] == "r":
            col = get_random_move(player, board)
            board.place_piece(col, player)
            
        elif players[player] == "m":
            val, pos = minimax.get_move(board, 4, player)
            board.place_piece(pos, player)
        
        player = (player + 1) % 2


def text_game_loop():
    board = Connect4()
    board.print_board()
    player = 0

    inp = int(input("\nPlayer " + str(player%2) + ", Drop a piece (1-7): "))
    while not board.is_there_a_winner():
        if board.is_open(inp):
            board.place_piece(inp, player%2)
            board.print_board()
            board.is_there_a_winner()
            p1, t1 = board.evaluate(0)
            p2, t2 = board.evaluate(1)
            p1k, t1k = board.evaluate_k(0)
            p2k, t2k = board.evaluate_k(1)

            print("V p1: " + str(p1) + " | V_K p1: " + str(p1k))
            print("V p2: " + str(p2) + " | V_K p2: " + str(p2k))
            print("Custom: [" + format(t1, ".2f") + "ms, " + format(t2, ".2f") + "ms]")
            print("Kernel: [" + format(t1k, ".2f") + "ms, " + format(t2k, ".2f") + "ms]")
            player = (player + 1) % 2
        else:
            print("no space to drop")
        if not board.is_there_a_winner():
            if players[player] == "p":
                get_player_move(player, board)
                
            elif players[player] == "r":
                get_random_move(player, board)

            elif players[player] == "m":
                val, pos = minimax.get_move(board, 4, player)
                board.place_piece(pos, player)
            
            player = (player + 1) % 2

def minimax_loop():
    board = Connect4()
    board.print_board()
    player = 0
    while not board.is_there_a_winner():
        if player == 0:
            inp = int(input("\nPlayer 0, Drop a piece (1-7): "))
            if board.is_open(inp):
                board.place_piece(inp, 0)
                player = (player+1)%2
            else:
                print("no space to drop")
        else:
            value, pos = minimax.get_move(board, 3, 1)
            board.place_piece(pos, 1)
            player = (player + 1) % 2
            board.print_board()

            p1 = board.evaluate(0)
            p2 = board.evaluate(1)
            p1k = board.evaluate_k(0)
            p2k = board.evaluate_k(1)

            print("V p1: " + str(p1) + " | V_K p1: " + str(p1k))
            print("V p2: " + str(p2) + " | V_K p2: " + str(p2k))
            #print("Custom: [" + format(t1, ".2f") + "ms, " + format(t2, ".2f") + "ms]")
            #print("Kernel: [" + format(t1k, ".2f") + "ms, " + format(t2k, ".2f") + "ms]")


def get_random_move(player, board):
    time.sleep(1)
    col = random.randint(1, 7)
    while(not board.is_open(col)):
        col = random.randint(1, 7)

    return int(col)
    
    
def get_player_move(player, board):
    inp = int(input("\nPlayer " + str(player % 2) + ", Drop a piece (1-7): "))
    while inp not in valid_inputs:
        inp = int(input("\nPlayer " + str(player%2) + ", Drop a piece (1-7): "))
    board.place_piece(inp, player)

def get_row_col_from_mouse(pos):
    x, y = pos
    col = (x - 66) // SQUARE_SIZE
    return col+1



def pyGameLoop():
    
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect Four++")
    game = Connect4(WIN)
    py_board = Board(WIN, 7, 6)
    clock = pygame.time.Clock()
    pygame.display.update()

    run_pygame_loop(game, clock, py_board)
    

def run_pygame_loop(game, clock, py_board):
    run = True
    player = 0

    while run:
        clock.tick(FPS)
        pygame.display.update()
        if game.is_there_a_winner():
            if game.check_winner(0):
                print(f'Player 0 is the winner... ({players[player]})')
            else:
                player = (player + 1) % 2
                print(f'Player 1 is the winner... ({players[player]})')
            pygame.quit()
            run = False

        if players[player] == "p":
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  #
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = get_row_col_from_mouse(pos)
                    if game.is_open(col):
                        row = game.place_piece(col, player)
                        py_board.place_piece(row, col, player)
                        player = (player + 1) % 2
                        print(col)
                    else:
                        print("no space to drop")
        elif players[player] == "m":
            val, pos = minimax.get_move(game, 4, player)
            row = game.place_piece(pos, player)
            py_board.place_piece(row, pos, player)
            player = (player + 1) % 2

        elif players[player] == "r":
            col = get_random_move(player, game)
            row = game.place_piece(col, player)
            py_board.place_piece(row, col, player)
            player = (player + 1) % 2

        





if __name__ == '__main__':
    main()