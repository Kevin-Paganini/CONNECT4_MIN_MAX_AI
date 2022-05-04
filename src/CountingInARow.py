class CountingInARow:
    """
    This heuristic takes in each column, row, and diagonal and sums the number of player pieces there are in them.

    4 in a row = 1000
    3 in a row = 3^3
    2 in a row = 2^3
    1 in a row = 0

    Any opponent pieces in any col, row, or diag invalidates the group, since it is impossible for that group
    to reach 4 in a row.

    This heuristic comes with some issues:
    -Minimax will prioritize blocking the opponent in (getting 2 potential 4 in a rows next turn, guaranteeing the win)
    -There is a situation with minimax vs minimax where one player will ignore an open 3 in a row and lose the game
        For this situation, there is somehow a smaller value than a loss, a double loss possibly?
        This means we need to bake in a priority to block a 4 in a row, regardless if there is a worse
        situation down the line.
        We do already have this in minimax, but clearly its being ignored for some reason
    -The points are completely random, and the 3rd power for 2 and 3 in a row is a random high enough value
    """

    def __init__(self, width, height, in_a_row):
        self.width = width
        self.height = height
        self.in_a_row = in_a_row

    def evaluate(self, board, player):
        total = 0
        total += self.eval_columns(board, player)
        total += self.eval_rows(board, player)
        total += self.eval_left_diag(board, player)
        total += self.eval_right_diag(board, player)

        total -= self.eval_columns(board, (player + 1) % 2)
        total -= self.eval_rows(board, (player + 1) % 2)
        total -= self.eval_left_diag(board, (player + 1) % 2)
        total -= self.eval_right_diag(board, (player + 1) % 2)

        return total

    def eval_columns(self, board, player):
        total = 0
        for x in range(self.width):
            for y in range(self.height-(self.in_a_row-1)):
                col = [board[y+i][x] for i in range(self.in_a_row)]
                if (player+1)%2 not in col:
                    col = list(map(lambda a: 0 if a == -1 else 1, col))
                    total += self.get_sum(col)
        return total

    def eval_rows(self, board, player):
        total = 0
        for y in range(self.height):
            for x in range(self.width-(self.in_a_row-1)):
                row = board[y][x:x+self.in_a_row]
                if (player+1)%2 not in row:
                    row = list(map(lambda a: 0 if a == -1 else 1, row))
                    total += self.get_sum(row)
        return total

    def eval_left_diag(self, board, player):   #left diag = \
        total = 0
        for y in range(self.height-(self.in_a_row-1)):
            for x in range(self.width-(self.in_a_row-1)):
                ldiag = [board[y+i][x+i] for i in range(self.in_a_row)]
                if (player+1)%2 not in ldiag:
                    ldiag = list(map(lambda a: 0 if a == -1 else 1, ldiag))
                    total += self.get_sum(ldiag)
        return total

    def eval_right_diag(self, board, player):   #right diag = /
        total = 0
        for y in range(self.height-(self.in_a_row-1)):
            for x in range(self.in_a_row-1, self.width):
                rdiag = [board[y+i][x-i] for i in range(self.in_a_row)]
                if (player+1)%2 not in rdiag:
                    rdiag = list(map(lambda a: 0 if a == -1 else 1, rdiag))
                    total += self.get_sum(rdiag)
        return total

    def get_sum(self, group):
        s = sum(group)
        if s == self.in_a_row:
            return 1000000
        elif s >= 2:
            return s**3
        else:
            return 0
