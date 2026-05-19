import random
from src.nmm.minimax import get_best_move
from src.nmm.evaluation import is_terminal, get_winner
from src.nmm.moves import apply_move, get_moves
from src.nmm.game import GameState

class RandomAI():
    def choose_move(self, game_state):
        return random.choice(get_moves(game_state)), 0

class MinimaxAI():
    def __init__(self, depth):
        self.depth = depth

    def choose_move(self, game_state):
        return get_best_move(game_state, self.depth)

class HeuristicAI():
    def choose_move(self, game_state):
        return random.choice(get_moves(game_state)), 0

def play_game(ai_x, ai_o, record=False):
    game = GameState()
    history = []

    while not is_terminal(game):

        if game.current_player == "X":
            move, score = ai_x.choose_move(game)
        else:
            move, score = ai_o.choose_move(game)

        if record:
            history.append({
                "player": game.current_player,
                "move": move,
                "board": game.board.copy(),
                "phase": game.phase,
                "score": score,
            })

        game = apply_move(game, move)

    return get_winner(game), game.move_count, history

def run_tournament(ai_x, ai_o, n_games=100, record_one=False):
    results = {
        "X_wins": 0,
        "O_wins": 0,
        "draws": 0,
        "lengths": []
    }

    replay = None

    for i in range(n_games):
        if record_one and i == 0:
            winner, length, replay = play_game(ai_x, ai_o, record=True)
        else:
            winner, length, _ = play_game(ai_x, ai_o, record=False)

        if winner == "X":
            results["X_wins"] += 1
        elif winner == "O":
            results["O_wins"] += 1
        else:
            results["draws"] += 1

        results["lengths"].append(length)

    return results, replay


def create_ai(ai_type, depth):
    if ai_type == "Random":
        return RandomAI()
    if ai_type == "Minimax":
        return MinimaxAI(depth)
    if ai_type == "Heuristic":
        return HeuristicAI()