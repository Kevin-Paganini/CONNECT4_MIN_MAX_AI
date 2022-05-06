from Connect4 import Connect4
import random
import time
import minimax
from CountingInARow import CountingInARow

FPS = 60
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
IN_A_ROW = 4

valid_inputs = [1, 2, 3, 4, 5, 6, 7]
players = ["p", "p"]


def main():
    while True:
        inp = input("Text(t), pygame(p), setPlayers(s), quit(q)?: ")
        if inp == "t":
            text_game_loop2()
        elif inp == 's':
            set_players()
        elif inp == "q":
            break


def set_players():
    player1choice = input("Plese enter player one choice (m for minimax, p for player, r for random): ")
    player2choice = input("Plese enter player two choice (m for minimax, p for player, r for random): ")
    players.clear()
    players.append(player1choice)
    players.append(player2choice)


def text_game_loop2():
    board = Connect4(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
    heur1 = CountingInARow(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
    board.print_board()
    player = 0
    num_moves = 0

    while not board.is_there_a_winner():
        print(f'Player: {player}')
        if players[player] == "p":
            get_player_move(player, board)
                
        elif players[player] == "r":
            col = get_random_move(board)
            board.place_piece(col, player)
            
        elif players[player] == "m":
            depth = num_moves // 4 + 3
            print(depth)
            if depth > 5:
                depth = 5
            val, pos = minimax.get_move(board, depth, player, heur1)
            board.place_piece(pos, player)
        
        player = (player + 1) % 2
        num_moves += 1
        board.print_board()
        p1 = board.evaluate(0, heur1)
        p2 = board.evaluate(1, heur1)
        print("V p1: " + str(p1) + "\nV p2: " + str(p2))


def get_random_move(board):
    time.sleep(1)
    col = random.randint(1, 7)
    while not board.is_open(col):
        col = random.randint(1, 7)
    return int(col)


def get_player_move(player, board):
    inp = int(input("\nPlayer " + str(player % 2) + ", Drop a piece (1-7): "))
    while inp not in valid_inputs:
        inp = int(input("\nPlayer " + str(player%2) + ", Drop a piece (1-7): "))
    board.place_piece(inp, player)


if __name__ == '__main__':
    main()