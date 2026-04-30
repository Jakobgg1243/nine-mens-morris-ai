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

def evaluate(state):
    if is_terminal(state):
        winner = get_winner(state)
        if winner == "X":   return  100000
        if winner == "O":   return -100000
        return 0

    X, O = "X", "O"

    material = state.on_board[X] - state.on_board[O]
    mills_x = count_mills(state, X)
    mills_o = count_mills(state, O)
    pot_x = potential_mills(state, X)
    pot_o = potential_mills(state, O)

    mob_x = get_moves_for_player(state, X)
    mob_o = get_moves_for_player(state, O)

    score = (
        material * 25 +
        (mills_x - mills_o) * 600 +
        (pot_x - pot_o) * 220 +
        (mob_x - mob_o) * 15
    )

    if state.phase == "placement":
        score += (pot_x - pot_o) * 60
        center = [4, 10, 13, 19]
        center_bonus = sum(1 for p in center if state.board[p] == X) - \
                       sum(1 for p in center if state.board[p] == O)
        score += center_bonus * 35

    else:
        score += material * 120
        if state.on_board[X] <= 3:
            score -= 20000
        if state.on_board[O] <= 3:
            score += 20000

    score += (state.move_count % 12) * 2

    return int(score)