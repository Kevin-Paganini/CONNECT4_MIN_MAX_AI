def get_move(board, limit, player):
    val, act = max_value(board, 0, player, limit)
    return val, act


def max_value(board, d, player, limit):
    if d == limit or board.is_there_a_winner():
        return [board.evaluate(player), None]

    v = -9223372036854775800
    act = None
    ply_player = (player + d) % 2
    for a in range(7):
        if board.is_open(a+1):
            val2, act2 = min_value(board.get_next_move(board, a+1, ply_player), d + 1, player, limit)
            #print(val2)
            if val2 > v:
                v = val2
                act = a+1
    return [v, act]


def min_value(board, d, player, limit):
    if d == limit or board.is_there_a_winner():
        return [board.evaluate(player), None]

    v = 9223372036854775800
    act = None
    ply_player = (player + d) % 2
    for a in range(7):
        if board.is_open(a+1):
            val2, act2 = max_value(board.get_next_move(board, a+1, ply_player), d + 1, player, limit)
            if val2 < v:
                v = val2
                act = a+1
    return [v, act]
