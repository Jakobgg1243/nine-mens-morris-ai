from src.nmm.game import GameState
from src.nmm.moves import get_moves, apply_move
from src.nmm.minimax import get_best_move
from src.nmm.evaluation import is_terminal, get_winner
from src.nmm.simulation import random_move, greedy_move, ai_vs_ai, ai_vs_random, ai_vs_greedy
import pygame
from src.nmm.pygame_display import PygameDisplay

def human_move_pygame(display: PygameDisplay, state: GameState):
    display.selected = None
    display.set_message("Your turn (X) - Click a point to place or move")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                idx = display.get_clicked_pos(event.pos)
                if idx is None:
                    continue

                moves = get_moves(state)

                if state.phase == "placement":
                    if any(m[0] == "place" and m[1] == idx for m in moves):
                        display.set_message("")
                        display.selected = None
                        return ("place", idx)

                else:
                    if display.selected is None:
                        if state.board[idx] == state.current_player:
                            display.selected = idx
                    else:
                        if idx == display.selected:
                            display.selected = None  
                        else:
                            move = ("move", display.selected, idx)
                            if move in moves:
                                display.selected = None
                                display.set_message("")
                                return move
                            elif state.board[idx] == state.current_player:
                                display.selected = idx  

        display.draw(state)

        pygame.time.wait(30)

def main():
    state = GameState()
    display = PygameDisplay()

    print("Nine Men's Morris")

    while True:
        display.draw(state)

        if is_terminal(state):
            winner = get_winner(state)
            msg = f"Game Over! {'You win!' if winner == 'X' else 'AI wins!' if winner == 'O' else 'Draw!'}"
            display.set_message(msg)
            display.draw(state)
            pygame.time.wait(4000)
            break

        if state.current_player == "X":
            move = human_move_pygame(display, state)
        else:
            display.set_message("AI (O) is thinking...")
            display.draw(state)
            pygame.time.wait(400)  

            move, _ = get_best_move(state, depth=4)

            if move is None:
                display.set_message("AI has no legal moves!")
                display.draw(state)
                pygame.time.wait(2000)
                break

            display.set_message(f"AI played: {move}")
            display.draw(state)
            pygame.time.wait(600)

        successors = apply_move(state, move)
        if not successors:
            print("Error applying move!")
            break

        state = successors[0]

    pygame.quit()


if __name__ == "__main__":
    main()
    #ai_vs_ai(depth_x=5, depth_o=4, games=10)    
    #ai_vs_random(ai_depth=5, games=10, ai_as_x=True)  
    #ai_vs_greedy(ai_depth=5, games=10, ai_as_x=True)