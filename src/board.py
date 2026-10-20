import pygame 
from piece import Piece
from constants import SQUARE_SIZE

DEFAULT_START_POS = [
    [Piece("b","R"), Piece("b","N"), Piece("b","B"), Piece("b","Q"), Piece("b","K"), Piece("b","B"), Piece("b","N"), Piece("b","R")],
    [Piece("b","P") for _ in range(8)],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [Piece("w","P") for _ in range(8)],
    [Piece("w","R"), Piece("w","N"), Piece("w","B"), Piece("w","Q"), Piece("w","K"), Piece("w","B"), Piece("w","N"), Piece("w","R")]
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
            for j, col in enumerate(row):
                if col:
                    screen.blit(self.piece_imgs[str(col)], (j*SQUARE_SIZE, i*SQUARE_SIZE))
