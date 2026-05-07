import streamlit as st
from src.nmm.ai_controller import get_ai_move
from src.nmm.moves import apply_move
from src.nmm.evaluation import is_terminal

def handle_ai_turn():
    if is_terminal(st.session_state.game):
        return

    if st.session_state.game.current_player == "O":
        move = get_ai_move(st.session_state.game)

        if move:
            st.session_state.game = apply_move(st.session_state.game, move)[0]
            st.session_state.game.last_move = move