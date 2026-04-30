from src.nmm.moves import get_moves, apply_move, is_mill
from src.nmm.evaluation import evaluate, is_terminal

def move_ordering_key(state, move):
    temp = state.copy()

    if move[0] == "place":
        temp.board[move[1]] = state.current_player
        score = 10
        if is_mill(temp.board, move[1]):
            score += 300          
    else:
        temp.board[move[1]] = " "
        temp.board[move[2]] = state.current_player
        score = 5
        if is_mill(temp.board, move[2]):
            score += 300

    return score


def minimax_alpha_beta(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(state):
        return evaluate(state), None
    
    moves = get_moves(state)
    if not moves:
        return evaluate(state), None
    
    moves.sort(key=lambda m: move_ordering_key(state, m), reverse=True)

    best_move = None

    if maximizing_player:  
        max_eval = -float('inf')
        for move in moves:
            successors = apply_move(state, move)
            if not successors:
                continue

            worst_case = float('inf')
            for s in successors:
                eval_score, _ = minimax_alpha_beta(s, depth - 1, alpha, beta, False)
                worst_case = min(worst_case, eval_score)

            if worst_case > max_eval:
                max_eval = worst_case
                best_move = move

            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
            
        return max_eval, best_move

    else:  
        min_eval = float('inf')
        for move in moves:
            successors = apply_move(state, move)
            if not successors:
                continue

            best_case = -float('inf')
            for s in successors:
                eval_score, _ = minimax_alpha_beta(s, depth - 1, alpha, beta, True)
                best_case = max(best_case, eval_score)

            if best_case < min_eval:
                min_eval = best_case
                best_move = move

            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        
        return min_eval, best_move


def get_best_move(state, depth=5):
    score, move = minimax_alpha_beta(state, depth, -float('inf'), float('inf'),
                                     maximizing_player=(state.current_player == "X"))
    return move, score