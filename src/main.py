from Connect4 import Connect4
import pygame


WIDTH = 1050
HEIGHT = 800
SQUARE_SIZE = WIDTH / 7

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
    row = y // SQUARE_SIZE
    col = (x + 50) // SQUARE_SIZE
    return col



def pyGameLoop():
    run = True
    game = Connect4(WIN)
    clock = pygame.time.Clock()
    

    pygame.display.update()
    while run:
        clock.tick(FPS)

        if game.turn == 0:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col  = get_row_col_from_mouse(pos)
                print(col)





if __name__ == '__main__':
    main()