from Connect4 import Connect4

def main():
    text_game_loop()

def text_game_loop():
    w = int(input("Enter board width (4+): "))
    h = int(input("Enter board height (4+): "))
    n = int(input("Enter number of pieces in a row to win (3+): "))

    board = Connect4(w,h,n)
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