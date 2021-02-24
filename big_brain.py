def get_bad_positions(board):
    bad_positions = []

    for x in range(board['width']):
        bad_positions.append({'x': x, 'y': -1})
        bad_positions.append({'x': x, 'y': (board['height'])})
    for y in range(board['height']):
        bad_positions.append({'x': -1, 'y': y})
        bad_positions.append({'x': (board['width']), 'y': y})

    for snake in board['snakes']:
        for position in snake['body']:
            bad_positions.append(position)

    for hazard in board['hazards']:
        bad_positions.append(hazard)

    return bad_positions

def get_next_moves(curr_position):
    return {
        'up': {
            'x': curr_position['x'],
            'y': (curr_position['y'] + 1)
        },
        'down': {
            'x': curr_position['x'],
            'y': (curr_position['y'] - 1)
        },
        'left': {
            'x': (curr_position['x'] - 1),
            'y': curr_position['y']
        },
        'right': {
            'x': (curr_position['x'] + 1),
            'y': curr_position['y']
        },
    }

def not_a_hole(me, next_position):
    next_moves = get_next_moves(next_position)

    me_positions = []
    for position in me['body']:
        if position != me['head']:
            me_positions.append(position)

    danger_zone = []
    for position in me_positions:
        if position in next_moves.values():
            danger_zone.append(position)

    if len(danger_zone) == 3:
        return False
    elif len(danger_zone) == 2:
        pos1 = danger_zone[0]
        pos2 = danger_zone[1]

        if pos1['x'] == pos2['x'] or pos1['y'] == pos2['y']:
            return False
        else:
            return True
    else:
        return True

def not_next_to_a_head(me, board, next_position):
    next_moves = get_next_moves(next_position)

    other_heads = []
    for snake in board['snakes']:
        if snake['head'] != me['head']:
            other_heads.append(snake['head'])

    danger_zone = []
    for position in other_heads:
        if position in next_moves.values():
            danger_zone.append(position)

    return len(danger_zone) == 0