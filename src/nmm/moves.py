from src.nmm.game import is_mill, ADJACENCY

def switch_player(player):
    return "O" if player == "X" else "X"

def get_moves(state):
    moves = []
    player = state.current_player

    if state.pending_removal:
        return [("remove", i) for i in state.removable_pieces]

    empties = [i for i in range(24) if state.board[i] == " "]

    if state.phase == "placement":
        return [("place", i) for i in empties]

    is_flying = (state.phase == "flying" and state.on_board[player] <= 3)

    for i in range(24):
        if state.board[i] == player:
            if is_flying:
                for j in empties:
                    moves.append(("move", i, j))
            else:
                for j in ADJACENCY.get(i, []):
                    if state.board[j] == " ":
                        moves.append(("move", i, j))

    return moves

def get_moves_for_player(state, player):
    temp_state = state.copy()
    temp_state.current_player = player
    return len(get_moves(temp_state))

def get_removable_pieces(state, opponent):
    removable = [i for i in range(24)
                 if state.board[i] == opponent and not is_mill(state.board, i)]

    if not removable:
        removable = [i for i in range(24) if state.board[i] == opponent]
    return removable

def apply_move(state, move):
    if move not in get_moves(state):
        return state
    
    new_history = state.move_history + [state.get_position_key()]
    new_state = state.copy()
    move_type = move[0]
    player = state.current_player
    opponent = switch_player(player)

    if move_type == "place":
        _, pos = move

        new_state.board[pos] = player
        new_state.placed[player] += 1
        new_state.on_board[player] += 1
        new_state.move_count += 1
        new_state.move_history = new_history

        if is_mill(new_state.board, pos):
            new_state.halfmove_clock = 0
            new_state.pending_removal = True
            new_state.removable_pieces = get_removable_pieces(new_state, opponent)
        else:
            new_state.halfmove_clock += 1
            new_state.current_player = opponent

        new_state.update_phase()
        return new_state

    elif move_type == "move":
        _, frm, to = move

        new_state.board[frm] = " "
        new_state.board[to] = player
        new_state.move_count += 1
        new_state.move_history = new_history

        if is_mill(new_state.board, to):
            new_state.halfmove_clock = 0
            new_state.pending_removal = True
            new_state.removable_pieces = get_removable_pieces(new_state, opponent)
        else:
            new_state.current_player = opponent

        new_state.update_phase()
        return new_state
    
    elif move_type == "remove":
        _, pos = move

        new_state.board[pos] = " "
        new_state.on_board[opponent] -= 1

        new_state.pending_removal = False
        new_state.removable_pieces = []
        new_state.current_player = opponent

        new_state.update_phase()
        return new_state
    
    else:
        raise ValueError(f"Invalid move: {move}")