from Connect4 import Connect4
import random
import time
import minimax
from CountingInARow import CountingInARow
from deepQ import DeepQLearning

#######################################################
# This is the continuation of the project
#######################################################



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
# Definitely more than 42 states I think
ql = DeepQLearning(states=42, actions=7, alpha=0.01, epsilon=.95, y=.95, batch_size=BATCH_SIZE, replay_mem_max=200, threshold=-5)








def train_deepQ():
    players = ["d", "m"]
    minimax_wins = 0
    deep_q_wins = 0
    for i in range(1000):


        board = Connect4(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
        heur1 = CountingInARow(BOARD_WIDTH, BOARD_HEIGHT, IN_A_ROW)
        board.print_board()
        player = 0

        while not board.is_there_a_winner():
            
                    
            if players[player] == "d":
                state = board.board.flatten()
                current_action = ql.get_action(state)
                current_action += 1
                col = current_action
                
                reward = 0

                if board.is_open(col):
                    
                    board.place_piece(col, player)
                    reward = board.evaluate(player, heur1)
                else:
                    reward = -1000
                    val, pos = minimax.get_move(board, 3, player, heur1)
                    board.place_piece(pos, player)
                
                

                # Train the model

                ql.update(state=state, reward=reward)
                ql.train_model()
                
            elif players[player] == "m":
                val, pos = minimax.get_move(board, 6, player, heur1)
                board.place_piece(pos, player)
            
            board.print_board()
            
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





if __name__ == '__main__':
    train_deepQ()
    