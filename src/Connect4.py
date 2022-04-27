import numpy as np

class Connect4():

    def __init__(self):
        #player 1 is 1
        #player 2 is 2
        # 0 is empty space
        self._board = np.zeros((6, 7))
        self.check_winner(1)
        # []


    def print_board(self):
        print(self._board)




    


    def check_winner(self, player):
        for idx, pos in np.ndenumerate(self._board):
            print(f'Index: {idx}, value: {pos}')
                
        return False

