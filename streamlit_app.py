import streamlit as st
from src.nmm.game import GameState
from src.nmm.evaluation import is_terminal, get_winner
from src.nmm.game_controller import handle_ai_turn
from src.nmm.moves import apply_move
from board_component import board_component
from src.nmm.tournament import create_ai, run_tournament

st.set_page_config(
    page_title="Nine Men's Morris",
    layout="centered",
)
st.title("Nine Men's Morris")

if "game" not in st.session_state:
    st.session_state.game = GameState()

if "ai_enabled" not in st.session_state:
    st.session_state.ai_enabled = True

game = st.session_state.game

winner = None
if is_terminal(game):
    winner = get_winner(game)

if winner == "X":
    st.success("🏆 You win!")
elif winner == "O":
    st.error("🤖 AI wins!")
elif winner is None and is_terminal(game):
    st.warning("Draw!")

click = board_component(
    board=game.board,
    phase=game.phase,
    current_player=game.current_player,
    removable=game.removable_pieces,
    ui_mode=game.ui_mode,
    last_move=game.last_move,
    key="board",
)

if "last_click" not in st.session_state:
    st.session_state.last_click = None

if click is not None and click != st.session_state.last_click:
    st.session_state.last_click = click

    if click["type"] == "place":
        game = apply_move(game, ("place", click["pos"]))
        game.last_move = ("place", click["pos"])

    elif click["type"] == "move":
        prev = game
        game = apply_move(game, ("move", click["from"], click["to"]))
        if game != prev:
            game.last_move = ("move", click["from"], click["to"])

    elif click["type"] == "remove":
        game = apply_move(game, ("remove", click["pos"]))
        game.last_move = ("remove", click["pos"])

    st.session_state.game = game
    st.rerun()

prev = st.session_state.game

if st.session_state.ai_enabled:
    handle_ai_turn()

if st.session_state.game != prev:
    st.rerun()

st.sidebar.subheader("Game")
st.sidebar.write(f"**Phase:** {st.session_state.game.phase}")
st.sidebar.write(f"**Current Player:** {st.session_state.game.current_player}")
st.sidebar.write(f"X placed: {st.session_state.game.placed['X']}/9")
st.sidebar.write(f"O placed: {st.session_state.game.placed['O']}/9")
st.sidebar.write(f"X on board: {st.session_state.game.on_board['X']}/9")
st.sidebar.write(f"O on board: {st.session_state.game.on_board['O']}/9")
st.session_state.ai_enabled = st.sidebar.checkbox(
    "Enable AI",
    value=st.session_state.ai_enabled
)

if st.sidebar.button("Reset Game"):
    st.session_state.game = GameState()
    st.rerun()

st.sidebar.header("AI Tournament")

ai_x_type = st.sidebar.selectbox("AI X", ["Minimax", "Random", "Heuristic"])
ai_o_type = st.sidebar.selectbox("AI O", ["Minimax", "Random", "Heuristic"])

depthX = depthO = 3
if ai_x_type == "Minimax":
    depthX = st.sidebar.slider("Minimax depth X", 1, 6, 3)
if ai_o_type == "Minimax":
    depthO = st.sidebar.slider("Minimax depth O", 1, 6, 3)

games = st.sidebar.number_input("Games", 10, 500, 20)

if st.sidebar.button("Run tournament"):

    ai_x = create_ai(ai_x_type, depthX)
    ai_o = create_ai(ai_o_type, depthO)

    results, replay = run_tournament(ai_x, ai_o, games, record_one=True)

    st.session_state.results = results
    st.session_state.replay = replay

if "results" in st.session_state:
    st.subheader("Tournament Results")
    st.write(st.session_state.results)

if "replay" in st.session_state and st.session_state.replay:
    replay = st.session_state.replay
    print(replay)
    