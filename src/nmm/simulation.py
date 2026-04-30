from src.nmm.game import GameState
from src.nmm.moves import get_moves, apply_move
from src.nmm.minimax import get_best_move
from src.nmm.evaluation import is_terminal, get_winner, evaluate
import random 

def random_move(state):
    moves = get_moves(state)
    if not moves:
        return None
    return random.choice(moves)


def greedy_move(state):
    moves = get_moves(state)
    if not moves:
        return None

    best_move = None
    best_score = -float('inf') if state.current_player == "X" else float('inf')
    maximizing = (state.current_player == "X")

    for move in moves:
        successors = apply_move(state, move)
        if not successors:
            continue

        worst_for_opponent = float('inf') if maximizing else -float('inf')

        for s in successors:
            score = evaluate(s)
            if maximizing:
                worst_for_opponent = min(worst_for_opponent, score)
            else:
                worst_for_opponent = max(worst_for_opponent, score)

        if maximizing:
            if worst_for_opponent > best_score:
                best_score = worst_for_opponent
                best_move = move
        else:
            if worst_for_opponent < best_score:
                best_score = worst_for_opponent
                best_move = move

    return best_move

def ai_vs_ai(depth_x=4, depth_o=5, games=5):
    for game_num in range(1, games + 1):
        state = GameState()
        move_number = 0
        print(f"\n=== Starting Game {game_num}/{games} ===")

        while not is_terminal(state):
            move_number += 1
            player = state.current_player

            if player == "X":
                depth = depth_x
            else:
                depth = depth_o

            print(f"Move {move_number:3d} | Phase: {state.phase:10} | "
                  f"X:{state.on_board['X']} O:{state.on_board['O']} | "
                  f"Since last mill: {state.halfmove_clock:2d} | "
                  f"{player} thinking (depth {depth})...", end="")

            move, score = get_best_move(state, depth=depth)

            if move is None:
                print(" No moves!")
                break

            successors = apply_move(state, move)
            if not successors:
                print(" Move failed!")
                break

            state = successors[0]

            print(f" played {move} | eval = {score}")

        winner = get_winner(state)
        result = "X wins" if winner == "X" else "O wins" if winner == "O" else "Draw"
        print(f"\nGame {game_num} finished: {result}  (Total moves: {state.move_count})")

    print("\nAI vs AI session completed.")

def ai_vs_random(ai_depth=5, games=10, ai_as_x=True):
    ai_wins = 0
    random_wins = 0
    draws = 0

    for game_num in range(1, games + 1):
        state = GameState()
        move_number = 0
        print(f"\n=== Game {game_num}/{games} ===")

        while not is_terminal(state):
            move_number += 1
            player = state.current_player

            print(f"Move {move_number:3d} | Phase: {state.phase:10} | "
                  f"X:{state.on_board['X']} O:{state.on_board['O']} | "
                  f"Since last mill: {state.halfmove_clock:2d} | ", end="")

            if (player == "X" and ai_as_x) or (player == "O" and not ai_as_x):
                print(f"AI ({player}) thinking (depth {ai_depth})...", end="")
                move, score = get_best_move(state, depth=ai_depth)
                print(f" played {move} | eval = {score}")
            else:
                print(f"Random ({player}) playing...", end="")
                move = random_move(state)
                print(f" played {move}")

            if move is None:
                print(" No legal moves!")
                break

            successors = apply_move(state, move)
            if not successors:
                print(" Move failed!")
                break

            state = successors[0]

        winner = get_winner(state)
        if winner == "X":
            if ai_as_x:
                ai_wins += 1
                result = "AI wins"
            else:
                random_wins += 1
                result = "Random wins"
        elif winner == "O":
            if ai_as_x:
                random_wins += 1
                result = "Random wins"
            else:
                ai_wins += 1
                result = "AI wins"
        else:
            draws += 1
            result = "Draw"

        print(f"Game {game_num} finished: {result}  (Total moves: {state.move_count})")

    print("\n" + "="*50)
    print("AI vs Random Results")
    print("="*50)
    if ai_as_x:
        print(f"AI (X, depth {ai_depth}) Wins : {ai_wins}")
        print(f"Random (O) Wins          : {random_wins}")
    else:
        print(f"AI (O, depth {ai_depth}) Wins : {ai_wins}")
        print(f"Random (X) Wins          : {random_wins}")
    print(f"Draws                    : {draws}")
    print("="*50)


def ai_vs_greedy(ai_depth=5, games=10, ai_as_x=True):
    ai_wins = 0
    greedy_wins = 0
    draws = 0

    for game_num in range(1, games + 1):
        state = GameState()
        print(f"\n=== Game {game_num}/{games} | AI depth {ai_depth} vs Greedy ===")

        while not is_terminal(state):
            if (state.current_player == "X" and ai_as_x) or (state.current_player == "O" and not ai_as_x):
                move, score = get_best_move(state, depth=ai_depth)
                print(f"AI ({state.current_player}) played {move} | eval {score}")
            else:
                move = greedy_move(state)
                print(f"Greedy ({state.current_player}) played {move}")

            if move is None:
                break

            successors = apply_move(state, move)
            if successors:
                state = successors[0]

        winner = get_winner(state)
        if winner == "X":
            result = "AI wins" if ai_as_x else "Greedy wins"

            if ai_as_x:
                ai_wins += 1
            else:
                greedy_wins += 1

        elif winner == "O":
            result = "Greedy wins" if ai_as_x else "AI wins"

            if ai_as_x:
                greedy_wins += 1
            else:
                ai_wins += 1

        else:
            result = "Draw"
            draws += 1

        print(f"Game {game_num} finished: {result} (Total moves: {state.move_count})")

    print("\n" + "="*60)
    print("AI vs Greedy Results")
    print("="*60)
    if ai_as_x:
        print(f"Minimax AI (X, depth {ai_depth}) Wins : {ai_wins}")
        print(f"Greedy AI (O) Wins                   : {greedy_wins}")
    else:
        print(f"Minimax AI (O, depth {ai_depth}) Wins : {ai_wins}")
        print(f"Greedy AI (X) Wins                   : {greedy_wins}")
    print(f"Draws                                 : {draws}")
    print("="*60)