
ADJACENCY = {
    0: [1, 9], 1: [0, 2, 4], 2: [1, 14],
    3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
    6: [7, 11], 7: [4, 6, 8], 8: [7, 12],
    9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15],
    12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
    15: [11, 16], 16: [15, 17, 19], 17: [12, 16],
    18: [10, 19], 19: [16, 18, 20, 22], 20: [13, 19],
    21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
}

MILLS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (9, 10, 11), (12, 13, 14), (15, 16, 17),
    (18, 19, 20), (21, 22, 23),
    (0, 9, 21), (3, 10, 18), (6, 11, 15),
    (1, 4, 7), (16, 19, 22),
    (8, 12, 17), (5, 13, 20), (2, 14, 23)
]


class GameState:
    def __init__(self):
        self.board = [" "] * 24
        self.current_player = "X"
        self.phase = "placement"
        self.placed = {"X": 0, "O": 0}
        self.on_board = {"X": 0, "O": 0}
        
        self.move_count = 0
        self.move_history = []          
        self.halfmove_clock = 0  

        self.ui_mode = "normal"
        self.pending_removal = False
        self.removable_pieces = []     

        self.last_move = None

    def copy(self):
        new_state = GameState()

        new_state.board = self.board.copy()
        new_state.current_player = self.current_player
        new_state.phase = self.phase

        new_state.placed = self.placed.copy()
        new_state.on_board = self.on_board.copy()

        new_state.move_count = self.move_count
        new_state.halfmove_clock = self.halfmove_clock

        new_state.move_history = self.move_history.copy()

        new_state.pending_removal = self.pending_removal
        new_state.removable_pieces = self.removable_pieces.copy()
        
        return new_state

    def get_position_key(self):
        return (tuple(self.board), self.current_player)

    def update_phase(self):
        if self.placed["X"] >= 9 and self.placed["O"] >= 9:
            if self.on_board["X"] <= 3 or self.on_board["O"] <= 3:
                self.phase = "flying"
            else:
                self.phase = "movement"

def is_mill(board, pos):
    for mill in MILLS:
        if pos in mill:
            a, b, c = mill
            if board[a] == board[b] == board[c] != " ":
                return True
    return False