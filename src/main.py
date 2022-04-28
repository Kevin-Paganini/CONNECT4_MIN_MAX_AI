from Connect4 import Connect4

def main():
    text_game_loop()

def text_game_loop():
    board = Connect4()
    board.print_board()
    pcount= 0

    inp = int(input("\nPlayer " + str(pcount%2) + ", Drop a piece (1-7): "))
    while(inp != 0):
        if(board.is_open(inp)):
            board.place_piece(int(inp), pcount%2)
            board.print_board()
            print("Value for player " + str(pcount%2 + 1) + ": " + str(board.evaluate(pcount%2)))
            print("Value for player " + str((pcount+1) % 2 + 1) + ": " + str(board.evaluate((pcount+1) % 2)))
            pcount += 1
        else:
            print("no space to drop")
        inp = int(input("\nPlayer " + str(pcount%2) + ", Drop a piece (1-7): "))



if __name__ == '__main__':
    main()