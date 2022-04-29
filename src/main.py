from Connect4 import Connect4
import pygame


WIDTH = 1050
HEIGHT = 800
SQUARE_SIZE = WIDTH / 7

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("Connect Four++")

valid_inputs = [1,2,3,4,5,6,7]

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
    row = y // SQUARE_SIZE          #FIXME clicking on some of the circles gives the wrong x,y coords
    col = (x + 50) // SQUARE_SIZE
    return row, col



def pyGameLoop():
    run = True
    game = Connect4(WIN)
    turn = 0                    #FIXME I would suggest updating turn in the game loop, not the board
    clock = pygame.time.Clock() #since we are passing in player to all game methods, instead of having it as an attr of connect4
    

    pygame.display.update()
    while run:
        clock.tick(FPS)

        if turn == 0:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                print(str(col) + " " + str(row))





if __name__ == '__main__':
    main()