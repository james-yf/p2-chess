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

    def handle_input(self, e):
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.board_img, (0,0))
        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if piece:
                    screen.blit(self.piece_imgs[piece], (j*SQUARE_SIZE, i*SQUARE_SIZE))
