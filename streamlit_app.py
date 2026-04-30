import streamlit as st

from src.nmm.game import GameState
from src.nmm.moves import apply_player_move, get_moves, apply_move
from src.nmm.minimax import get_best_move

if "game" not in st.session_state:
    st.session_state.game = GameState()

state = st.session_state.game

st.title("Nine Men's Morris")

st.write("Current player:", state.current_player)
st.write(state.board)

cols = st.columns(6)

for i in range(24):
    col = cols[i % 6]

    label = state.board[i]

    if label == " ":
        label = str(i)

    if col.button(label, key=i):

        move = ("place", i)

        legal_moves = get_moves(state)

        if move in legal_moves:
            st.session_state.game = apply_player_move(state, move)

            st.rerun()
        st.write("Clicked:", i)

if st.session_state.game.current_player == "O":

    with st.spinner("AI thinking..."):

        move, score = get_best_move(
            st.session_state.game,
            depth = 4
        )

        successors = apply_move(
            st.session_state.game,
            move
        )

        st.session_state.game = successors[0]

        st.rerun()

if st.button("Restart Game"):
    st.session_state.game = GameState()
    st.rerun()