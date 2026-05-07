from src.nmm.game import is_mill, ADJACENCY

def switch_player(player):
    return "O" if player == "X" else "X"

def get_moves(state):
    moves = []
    player = state.current_player
    empties = [i for i in range(24) if state.board[i] == " "]

    if state.phase == "placement":
        for pos in empties:
            moves.append(("place", pos))
        return moves

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


def get_removable_pieces(state, opponent):
    removable = [i for i in range(24)
                 if state.board[i] == opponent and not is_mill(state.board, i)]

    if not removable:
        removable = [i for i in range(24) if state.board[i] == opponent]
    return removable


def apply_move(state, move):
    new_history = state.move_history + [state.get_position_key()]
    
    move_type = move[0]

    if move_type == "place":
        _, pos = move
        new_state = state.copy()
        new_state.board[pos] = state.current_player
        new_state.placed[state.current_player] += 1
        new_state.on_board[state.current_player] += 1
        new_state.move_count += 1
        new_state.move_history = new_history
        new_state.update_phase()
        if is_mill(new_state.board, pos):
            new_state.halfmove_clock = 0
            opponent = switch_player(state.current_player)
            removable = get_removable_pieces(new_state, opponent)
            return [create_removal_state(new_state, r, opponent) for r in removable]
        else:
            new_state.halfmove_clock += 1
            new_state.current_player = "O" if state.current_player == "X" else "X"
            return [new_state]

    elif move_type == "move":
        _, frm, to = move
        new_state = state.copy()
        new_state.board[frm] = " "
        new_state.board[to] = state.current_player
        new_state.move_count += 1
        new_state.move_history = new_history

        if is_mill(new_state.board, to):
            new_state.halfmove_clock = 0
            opponent = switch_player(state.current_player)
            removable = get_removable_pieces(new_state, opponent)
            return [create_removal_state(new_state, r, opponent) for r in removable]
        else:
            new_state.halfmove_clock += 1
            new_state.current_player = "O" if state.current_player == "X" else "X"
            return [new_state]

    return []

def apply_player_move(state, move):
    new_state = state.copy()

    move_type = move[0]

    if move_type == "place":
        if move not in get_moves(state):
            return state
        
        _, pos = move
        new_state.board[pos] = state.current_player
        new_state.placed[state.current_player] += 1
        new_state.on_board[state.current_player] += 1
        new_state.move_count += 1

        if is_mill(new_state.board, pos):
            opponent = switch_player(state.current_player)
            removable = get_removable_pieces(new_state, opponent)
            new_state.pending_removal = True
            new_state.removable_pieces = removable
            new_state.ui_mode = "removal"
            return new_state

        new_state.current_player = switch_player(state.current_player)
        new_state.halfmove_clock += 1
        new_state.update_phase()

        return new_state

    elif move_type == "move":
        if move not in get_moves(state):
            return state
        
        _, frm, to = move
        new_state.board[frm] = " "
        new_state.board[to] = state.current_player
        new_state.move_count += 1

        if is_mill(new_state.board, to):
            opponent = switch_player(state.current_player)
            removable = get_removable_pieces(new_state, opponent)
            new_state.pending_removal = True
            new_state.removable_pieces = removable
            new_state.ui_mode = "removal"
            return new_state

        new_state.current_player = switch_player(state.current_player)
        new_state.halfmove_clock += 1
        new_state.update_phase()

        return new_state
    
    elif move_type == "remove":
        _, pos = move
        if pos not in state.removable_pieces:
            return state
        
        opponent = switch_player(state.current_player)
        new_state.board[pos] = " "
        new_state.on_board[opponent] -= 1
        new_state.pending_removal = False
        new_state.removable_pieces = []
        new_state.current_player = opponent
        new_state.halfmove_clock = 0
        new_state.update_phase()

        return new_state
    
    return new_state

def create_removal_state(base_state, remove_pos, opponent):
    temp = base_state.copy()
    temp.board[remove_pos] = " "
    temp.on_board[opponent] -= 1
    temp.current_player = opponent
    temp.halfmove_clock = 0                     
    temp.update_phase()
    return temp

def get_moves_for_player(state, player):
    temp_state = state.copy()
    temp_state.current_player = player
    return len(get_moves(temp_state))
