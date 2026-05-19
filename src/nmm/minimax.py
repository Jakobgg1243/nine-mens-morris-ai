from src.nmm.moves import get_moves, apply_move
from src.nmm.evaluation import evaluate, is_terminal

transposition_table = {}

def minimax_alpha_beta(state, depth, alpha, beta, maximizing_player):
    key = (state.get_position_key(), depth, maximizing_player)
    if key in transposition_table:
        return transposition_table[key]

    if depth == 0 or is_terminal(state):
        result = (evaluate(state), None)
        transposition_table[key] = result
        return result

    moves = get_moves(state)
    if not moves:
        return evaluate(state), None

    best_move = None

    if maximizing_player:
        max_eval = -float('inf')

        for move in moves:
            next_state = apply_move(state, move)

            eval_score, _ = minimax_alpha_beta(
                next_state, depth - 1, alpha, beta, False
            )

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, max_eval)

            if beta <= alpha:
                break

        transposition_table[key] = (max_eval, best_move)
        return max_eval, best_move

    else:
        min_eval = float('inf')

        for move in moves:
            next_state = apply_move(state, move)

            eval_score, _ = minimax_alpha_beta(
                next_state, depth - 1, alpha, beta, True
            )

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, min_eval)

            if beta <= alpha:
                break

        
        transposition_table[key] = (min_eval, best_move)
        return min_eval, best_move


def get_best_move(state, depth=5):
    score, move = minimax_alpha_beta(state, depth, -float('inf'), float('inf'),
                                     maximizing_player=(state.current_player == "X"))
    return move, score