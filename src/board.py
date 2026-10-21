import pygame 
from constants import SQUARE_SIZE

DEFAULT_START_POS = [
    ["bR","bN","bB","bQ","bK","bB","bN","bR"],
    ["bP"] * 8, 
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ["wP"] * 8, 
    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]

class Board:
    def __init__(self, board_img, piece_imgs, start_pos):
        self.board_img = board_img 
        self.piece_imgs = piece_imgs
        self.grid = start_pos 
        self.selected_sq = None

    def is_sq_empty(self, sq):
        sq_row, sq_col = sq
        return not self.grid[sq_row][sq_col]

    def handle_click(self, clicked_sq):
        if clicked_sq == self.selected_sq or self.is_sq_empty(clicked_sq):
            self.selected_sq = None
            return
        self.selected_sq = clicked_sq

    def draw(self, screen):
        screen.blit(self.board_img, (0,0))

        if self.selected_sq:
            sq_row, sq_col = self.selected_sq
            pygame.draw.rect(screen, (0,255,0), (sq_col*SQUARE_SIZE, sq_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if piece:
                    screen.blit(self.piece_imgs[piece], (j*SQUARE_SIZE, i*SQUARE_SIZE))

