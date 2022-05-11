
#######################################################
# General purpose file for training, collecting data, and command prompt version
#######################################################



from Connect4 import Connect4
import random
import time
import minimax
from CountingInARow import CountingInARow
from deepQ import DeepQLearning





WIDTH = 1050
HEIGHT = 800
SQUARE_SIZE = 133
FPS = 60
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
IN_A_ROW = 4

valid_inputs = [1, 2, 3, 4, 5, 6, 7]
players = ["m", "r"]
BATCH_SIZE = 16
ql = DeepQLearning(states=42, actions=7, alpha=0.01, epsilon=.95, y=.95, batch_size=BATCH_SIZE, replay_mem_max=200, threshold=-5)



def main():
    while True:
        inp = input("Text(t), setPlayers(s), quit(q), collect data(c)?: ")
        if inp == "t":
            text_game_loop2()
        elif inp == "s":
            setPlayers()
        elif inp == "c":
            collect_data()
        elif inp == "q":
            break
    text_game_loop2()
    

# Function to set players
def setPlayers():
    player1choice = input("Plese enter player one choice (m for minimax, p for player, r for random): ")
    player2choice = input("Plese enter player two choice (m for minimax, p for player, r for random): ")
    players.clear()
    players.append(player1choice)
    players.append(player2choice)

# general purpose function to test stuff out
def text_game_loop2():
    players = ["m", "r"]
    minimax_wins = 0
    random_wins = 0
    

    board = Connect4(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
    heur1 = CountingInARow(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
    #board.print_board()
    player = 0

    while not board.is_there_a_winner():
        #print(f'Player: {player}')
        if players[player] == "p":
            get_player_move(player, board)
                
        elif players[player] == "r":
            col = get_random_move(player, board)
            board.place_piece(col, player)
            
        elif players[player] == "m":
            val, pos = minimax.get_move(board, 1, player, heur1)
            board.place_piece(pos, player)
        
        player = (player + 1) % 2
        #board.print_board()
        #p1 = board.evaluate(0, heur1)
        #p2 = board.evaluate(1, heur1)
        #print("V p1: " + str(p1) + "\nV p2: " + str(p2))
    if board.is_there_a_winner():
        if board.check_winner(0):
            print(f'Player 0 win')
            minimax_wins += 1
        else:
            print(f'Player 1 win')
            random_wins += 1
    
# method used to train deep Q 
# (DON'T GRADE US ON THIS, THIS IS THE CONTINUATION OF PROJECT)
def train_deepQ():
    players = ["d", "m"]
    minimax_wins = 0
    deep_q_wins = 0
    for i in range(1000):


        board = Connect4(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
        heur1 = CountingInARow(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
        #board.print_board()
        player = 0

        while not board.is_there_a_winner():
            
                    
            if players[player] == "d":
                state = board.board.flatten()
                current_action = ql.get_action(state)
                current_action += 1
                col = current_action
                board.place_piece(col, player)
                reward = 0

                if board.is_open(col):
                    time.sleep(0.2)
                    board.place_piece(col, player)
                    reward = board.evaluate(player, heur1)
                else:
                    reward = -100
                    val, pos = minimax.get_move(board.board, 3, player, heur1)
                    board.place_piece(pos, player)
                player = (player + 1) % 2
                

                # Train the model

                ql.update(state=state, reward=reward)
                ql.train_model()
                
            elif players[player] == "m":
                val, pos = minimax.get_move(board, 6, player, heur1)
                board.place_piece(pos, player)
            
            player = (player + 1) % 2
            
        if board.is_there_a_winner():
            if board.check_winner(0):
                print(f'Player 0 win')
                deep_q_wins += 1
            else:
                print(f'Player 1 win')
                minimax_wins += 1

    print(f'Deep q wins: {deep_q_wins}')  
    print(f'Minimax wins: {minimax_wins}')
    
# Random player move
def get_random_move(player, board):
    time.sleep(1)
    col = random.randint(1, 7)
    while not board.is_open(col):
        col = random.randint(1, 7)
    return int(col)

# Player move
def get_player_move(player, board):
    inp = int(input("\nPlayer " + str(player % 2) + ", Drop a piece (1-7): "))
    while inp not in valid_inputs:
        inp = int(input("\nPlayer " + str(player%2) + ", Drop a piece (1-7): "))
    board.place_piece(inp, player)

# Method used to collect data in different ways
def collect_data():
    for i in range(10):
        board = Connect4(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
        heur1 = CountingInARow(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
        board.print_board()
        player = 0
        count = 0
        run = True
        rate = 0.4
        players = ["m", "m"]
        with open("data_min_max6_v_min_max6.txt", "a") as f:
            while run:
                

                if players[player] == "r":
                    count += 1
                    if board.is_there_a_winner():
                        run = False

                    if count % 2 == 0:

                        if random.random() > 0.2:

                            val, pos = minimax.get_move(board, 3, player, heur1)
                            board.place_piece(pos, player)
                        else:
                            pos = get_random_move(player, board)
                            board.place_piece(pos, player)
                    else:
                        if random.random() < rate:

                            pos = get_random_move(player, board)
                            board.place_piece(pos, player)
                        else:
                            val, pos = minimax.get_move(board, 1, player, heur1)
                            board.place_piece(pos, player)
                    f.write(str(pos) + ", ")
                                    
                    
                elif players[player] == "m":
                    if board.is_there_a_winner():
                        run = False
                    val, pos = minimax.get_move(board, 6, player, heur1)
                    board.place_piece(pos, player)
                    f.write(str(pos) + ", ")
                    
                player = (player + 1) % 2
                board.print_board()
                
                if board.is_there_a_winner():
                    run = False
               
                
            
            if board.is_there_a_winner():
                
                if board.check_winner(0):
                    f.write(str(0))
                else:
                    f.write(str(1))
            else:
                f.write(str(-1))
            f.write("\n")

           


if __name__ == '__main__':
    
    main()