from Connect4 import Connect4
from main import BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW
import numpy as np

DEBUG = False


def parse_data():
    games = read_data_in()
    with open("boards_and_targets.txt", "w") as w:
        for game in games:
            connect_4 = Connect4(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
            moves = game.split(", ")
            print(moves)
            player = 0
            for i in range(len(moves) - 1):
                if i % 2 == 0:

                
                    if not connect_4.is_there_a_winner():
                        board = connect_4.board
                        player = (player + 1) % 2
                        flat_board = np.array(board).reshape(-1)
                        np_flat_board_string = np.array2string(flat_board, separator=',',suppress_small=True)
                        np_flat_board_string = np_flat_board_string.replace('[', '')
                        np_flat_board_string = np_flat_board_string.replace(']', '')
                        np_flat_board_string = np_flat_board_string.replace('\n', '')
                        np_flat_board_string = np_flat_board_string.replace(' ', '')
                        to_write = f'{np_flat_board_string}'
                        to_write += ', '
                        to_write += f'{moves[i]}'

                        w.write(to_write)
                        w.write(f'\n')
                        connect_4.place_piece(int(moves[i]),player)
                    
                    
                
                

                


def read_data_in():
    with open("data.txt") as r:
        to_parse = r.read()
        games = to_parse.split("\n")
        i = 0
        if DEBUG:
            for game in games:
                print(f'Game {i}: {game}')
                i += 1
    return games


if __name__ == "__main__":
    parse_data()