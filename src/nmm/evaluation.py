from src.nmm.moves import get_moves_for_player
from src.nmm.game import MILLS, ADJACENCY

def is_terminal(state):
    if state.on_board["X"] < 3 and state.placed["X"] >= 9:
        return True
    if state.on_board["O"] < 3 and state.placed["O"] >= 9:
        return True
    if get_moves_for_player(state, state.current_player) == 0:
        return True
    if is_threefold_repetition(state):
        return True
    if state.move_count > 300:
        return True
    return False

def get_winner(state):
    if state.on_board["X"] < 3 and state.placed["X"] >= 9:
        return "O"
    if state.on_board["O"] < 3 and state.placed["O"] >= 9:
        return "X"
    if get_moves_for_player(state, state.current_player) == 0:
        return "O" if state.current_player == "X" else "X"
    
    if is_threefold_repetition(state) or state.move_count > 300:
        return None   
    return None

def is_threefold_repetition(state):
    if len(state.move_history) < 6:
        return False
    current = state.get_position_key()
    count = sum(1 for past in state.move_history if past == current)
    return count >= 3

def count_mills(state, player):
    return sum(1 for a, b, c in MILLS if state.board[a] == state.board[b] == state.board[c] == player)

def potential_mills(state, player):
    count = 0
    for a, b, c in MILLS:
        pieces = [state.board[a], state.board[b], state.board[c]]
        if pieces.count(player) == 2 and pieces.count(" ") == 1:
            count += 1
    return count

def mobility(state, player):
    return get_moves_for_player(state, player)

def blocked_pieces(state, player):
    blocked = 0
    for i in range(24):
        if state.board[i] == player:
            if not any(state.board[n] == " " for n in ADJACENCY.get(i, [])):
                blocked += 1
    return blocked

WIN_SCORE = 1_000

def evaluate(state):
    if is_terminal(state):
        winner = get_winner(state)
        if winner == "X":
            return WIN_SCORE
        if winner == "O":
            return -WIN_SCORE
        return 0

    X, O = "X", "O"

    material = (state.on_board[X] - state.on_board[O]) / 9

    mills_x = count_mills(state, X)
    mills_o = count_mills(state, O)
    mills = (mills_x - mills_o) / 4   

    pot_x = potential_mills(state, X)
    pot_o = potential_mills(state, O)
    potential = (pot_x - pot_o) / 8

    mob_x = get_moves_for_player(state, X)
    mob_o = get_moves_for_player(state, O)

    mobility_score = (mob_x - mob_o) / (mob_x + mob_o + 1)

    blocked_x = blocked_pieces(state, X)
    blocked_o = blocked_pieces(state, O)
    blocked = (blocked_o - blocked_x) / 9

    center = [4, 10, 13, 19]
    center_score = (
        sum(1 for p in center if state.board[p] == X)
        - sum(1 for p in center if state.board[p] == O)
    ) / 4

    placement_weight = 1.0 if state.phase == "placement" else 0.3

    score = ( material * 0.25 + 
             mills * 0.55 + 
             potential * 0.20 + 
             mobility_score * 0.35 + 
             blocked * 0.20 + 
             center_score * 0.10 * placement_weight)

    score *= WIN_SCORE

    return int(score)