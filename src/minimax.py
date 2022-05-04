def get_move(board, limit, player, heur):
    alpha = -9223372036854775800
    beta = 9223372036854775800
    val, act = max_value(board, 0, player, limit, alpha, beta, heur)
    return val, act


def max_value(board, d, player, limit, alpha, beta, heur):
    if d == limit or board.is_there_a_winner():
        return [board.evaluate(player, heur), None]

    v = -9223372036854775800
    act = None
    ply_player = (player + d) % 2
    for a in range(7): # all possible moves
        if board.is_open(a+1):
            val2, act2 = min_value(board.get_next_move(board, a+1, ply_player), d + 1, player, limit, alpha, beta, heur)
            #print(val2)
            if val2 > v:
                v = val2
                act = a+1
                alpha = max(alpha, v)
            if v >= beta:
                return [v, act]
    return [v, act]


def min_value(board, d, player, limit, alpha, beta, heur):
    if d == limit or board.is_there_a_winner():
        return [board.evaluate(player, heur), None]

    v = 9223372036854775800
    act = None
    ply_player = (player + d) % 2
    for a in range(7): # all possible moves
        if board.is_open(a+1):
            val2, act2 = max_value(board.get_next_move(board, a+1, ply_player), d + 1, player, limit, alpha, beta, heur)
            if val2 < v:
                v = val2
                act = a+1
                beta = min(beta, v)
            if v <= alpha:
                return [v, act]
    return [v, act]
