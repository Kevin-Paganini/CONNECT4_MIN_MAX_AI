

################################################
# Custom implementation of mini-max from Aaron and Kevin
################################################


# Starts the search algorithm and returns a move
def get_move(board, limit, player, heur):
    alpha = -9223372036854775800
    beta = 9223372036854775800
    val, act = max_value(board, 0, player, limit, alpha, beta, heur)
    return val, act

# Finds maximal board
def max_value(board, d, player, limit, alpha, beta, heur):
    if d == limit or board.is_there_a_winner():
        if d == 0:
            d = 0.000001
        return [board.evaluate(player, heur)/d, None]

    v = -9223372036854775800
    act = None
    ply_player = (player + d) % 2
    for a in range(7): # all possible moves
        if board.is_open(a+1):
            # We added heuristic here, because we wanted to try out some different ones
            val2, act2 = min_value(board.get_next_move(board, a+1, ply_player), d + 1, player, limit, alpha, beta, heur)
            
            if val2 > v:
                v = val2
                act = a+1
                alpha = max(alpha, v) # ALPHA-BETA PRUNING
            if v >= beta:
                return [v, act]
    return [v, act]


# Finds minimal board
def min_value(board, d, player, limit, alpha, beta, heur):
    if d == limit or board.is_there_a_winner():
        if d == 0:
            d = 0.000001
        return [board.evaluate(player, heur)/d, None]

    v = 9223372036854775800
    act = None
    ply_player = (player + d) % 2
    for a in range(7): # all possible moves
        if board.is_open(a+1):
            # We added heuristic here, because we wanted to try out some different ones
            val2, act2 = max_value(board.get_next_move(board, a+1, ply_player), d + 1, player, limit, alpha, beta, heur)
            if val2 < v:
                v = val2
                act = a+1
                beta = min(beta, v) #ALPHA-BETA PRUNING
            if v <= alpha:
                return [v, act]
    return [v, act]
