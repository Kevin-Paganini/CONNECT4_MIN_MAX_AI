from Connect4 import Connect4

def main():
    board = Connect4()
    board.print_board()

    board.place_piece(1, 1)
    board.place_piece(1, 2)
    board.place_piece(1, 1)
    board.place_piece(1, 2)
    board.place_piece(1, 1)
    board.print_board()


if __name__ == '__main__':
    main()