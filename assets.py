import pygame
from constants import SCREEN_W, SCREEN_H, SQUARE_SIZE

class AssetManager:
    def __init__(self):
        self.icon = None
        self.board_img = None
        self.piece_imgs = {}

    def load_all(self):
        icon = pygame.image.load("assets/icon.png")
        self.icon = pygame.transform.scale(icon, (32,32))

        board_img = pygame.image.load("assets/board.svg")
        self.board_img = pygame.transform.scale(board_img, (SCREEN_W, SCREEN_H))

        piece_initials = ["R","N","B","Q","K","P"] 
        colors = ["b","w"]
        for initial in piece_initials:
            for color in colors:
                name = f"{color}{initial}"
                img = pygame.image.load(f"assets/pieces/{name}.svg")
                img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                self.piece_imgs[name] = img
