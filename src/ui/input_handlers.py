import streamlit as st
from src.nmm.moves import apply_move, get_moves

def placement_ui(game):
    pos = st.number_input("Enter position from console", min_value=0, max_value=23, step=1, key="manual_pos")

    if st.button("Place Piece at this position", type="primary"):
        if game.board[pos] == " ":   
            st.session_state.game = apply_move(game, ("place", pos))[0]
            st.rerun()
        else:
            st.warning(f"Position {pos} is already occupied!")

def movement_ui(game):
    from_pos = st.number_input("Move FROM", min_value=0, max_value=23, step=1, key="from_pos")
    to_pos = st.number_input("Move TO", min_value=0, max_value=23, step=1, key="to_pos")

    if st.button("Move Piece", type="primary"):

        legal_moves = [m for m in get_moves(game) if m == ("move", from_pos, to_pos)]

        if legal_moves:
            st.session_state.game = apply_move(game,("move", from_pos, to_pos))[0]

            st.rerun()

        else:
            st.warning("Illegal move")