import streamlit as st
from src.nmm.game import GameState
from src.nmm.evaluation import is_terminal, get_winner
from src.ui.board_renderer import render_board
from src.ui.input_handlers import placement_ui, movement_ui
from src.nmm.game_controller import handle_ai_turn

st.set_page_config(page_title="Nine Men's Morris", layout="centered")
st.title("🪨 Nine Men's Morris")

if "game" not in st.session_state:
    st.session_state.game = GameState()

handle_ai_turn()

winner = None
if is_terminal(st.session_state.game):
    winner = get_winner(st.session_state.game)

if winner == "X":
    st.success("🏆 You win!")
elif winner == "O":
    st.error("🤖 AI wins!")
elif winner is None and is_terminal(st.session_state.game):
    st.warning("Draw!")

st.iframe(render_board(st.session_state.game), height=790)


if not is_terminal(st.session_state.game):
    if st.session_state.game.phase == "placement":
        placement_ui(st.session_state.game)
    else:
        movement_ui(st.session_state.game)

st.sidebar.subheader("Game")
st.sidebar.write(f"**Phase:** {st.session_state.game.phase}")
st.sidebar.write(f"**Current Player:** {st.session_state.game.current_player}")
st.sidebar.write(f"X placed: {st.session_state.game.placed['X']}/9")
st.sidebar.write(f"O placed: {st.session_state.game.placed['O']}/9")
st.sidebar.write(f"X on board: {st.session_state.game.on_board['X']}/9")
st.sidebar.write(f"O on board: {st.session_state.game.on_board['O']}/9")

if st.sidebar.button("Reset Game"):
    st.session_state.game = GameState()
    st.rerun()
