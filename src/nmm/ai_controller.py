from src.nmm.minimax import get_best_move

def get_ai_move(game):
    move, score = get_best_move(game, depth=4)
    return move