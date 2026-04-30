import pygame
import sys
from src.nmm.game import ADJACENCY

BG_COLOR = (15, 25, 40)
LINE_COLOR = (220, 190, 120)
TEXT_COLOR = (245, 245, 245)

X_COLOR = (220, 60, 60)   
O_COLOR = (60, 160, 220)  

HIGHLIGHT_COLOR = (255, 255, 100)
SELECT_COLOR = (100, 255, 120)

class PygameDisplay:
    def __init__(self, width=820, height=740):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Nine Men's Morris")

        self.font = pygame.font.SysFont("segoeui", 28, bold=True)
        self.small_font = pygame.font.SysFont("segoeui", 20)
        
        self.piece_font = pygame.font.SysFont("arial", 52, bold=True)

        self.positions = self.create_positions()
        self.point_radius = 17
        self.selected = None
        self.message = ""

    def create_positions(self):
        cx = self.width // 2
        cy = self.height // 2 - 25
        outer = 265
        mid = 150
        inner = 58

        return [
            (cx - outer, cy - outer), (cx, cy - outer), (cx + outer, cy - outer),   
            (cx - mid,   cy - mid),   (cx, cy - mid),   (cx + mid,   cy - mid),     
            (cx - inner, cy - inner), (cx, cy - inner), (cx + inner, cy - inner),   
            (cx - outer, cy),         (cx - mid, cy),   (cx - inner, cy),           
            (cx + inner, cy),         (cx + mid, cy),   (cx + outer, cy),           
            (cx - inner, cy + inner), (cx, cy + inner), (cx + inner, cy + inner),   
            (cx - mid,   cy + mid),   (cx, cy + mid),   (cx + mid,   cy + mid),     
            (cx - outer, cy + outer), (cx, cy + outer), (cx + outer, cy + outer),   
        ]

    def draw_lines(self):
        p = self.positions
        thick = 7

        drawn = set()
        for start in range(24):
            for end in ADJACENCY.get(start, []):
                if (start, end) not in drawn and (end, start) not in drawn:
                    pygame.draw.line(self.screen, LINE_COLOR, p[start], p[end], thick)
                    drawn.add((start, end))

    def draw_pieces(self, state):
        for i, piece in enumerate(state.board):
            if piece == " ":
                continue

            x, y = self.positions[i]
            color = X_COLOR if piece == "X" else O_COLOR

            text = self.piece_font.render(piece, True, color)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

    def draw(self, state):
        self.screen.fill(BG_COLOR)
        self.draw_lines()
        self.draw_pieces(state)

        if self.selected is not None:
            pygame.draw.circle(self.screen, SELECT_COLOR, self.positions[self.selected], 
                             self.point_radius + 12, 5)

        if self.selected is not None:
            legal = self.get_legal_targets(state, self.selected)
            for tgt in legal:
                pygame.draw.circle(self.screen, HIGHLIGHT_COLOR, self.positions[tgt], 10, 3)

        self.draw_info(state)
        pygame.display.flip()

    def get_legal_targets(self, state, from_pos):
        if state.phase == "placement":
            return []
        player = state.current_player
        if state.phase == "flying" and state.on_board[player] <= 3:
            return [i for i in range(24) if state.board[i] == " "]

        return [n for n in ADJACENCY.get(from_pos, []) if state.board[n] == " "]

    def draw_info(self, state):
        title = self.font.render("Nine Men's Morris", True, TEXT_COLOR)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 15))

        phase = self.small_font.render(f"Phase: {state.phase.capitalize()}", True, TEXT_COLOR)
        turn = self.small_font.render(f"Turn: {'You (X)' if state.current_player == 'X' else 'AI (O)'}", True, TEXT_COLOR)

        self.screen.blit(phase, (40, 625))
        self.screen.blit(turn, (40, 655))

        pieces = self.small_font.render(f"X: {state.on_board['X']}    O: {state.on_board['O']}", True, TEXT_COLOR)
        self.screen.blit(pieces, (self.width - 200, 625))

        if self.message:
            msg = self.small_font.render(self.message, True, (255, 230, 80))
            self.screen.blit(msg, (self.width//2 - msg.get_width()//2, 690))

    def get_clicked_pos(self, mouse_pos):
        mx, my = mouse_pos
        for i, (x, y) in enumerate(self.positions):
            dist = (mx - x)**2 + (my - y)**2
            if dist <= (self.point_radius + 20)**2:   
                return i
        return None

    def set_message(self, text):
        self.message = text

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()