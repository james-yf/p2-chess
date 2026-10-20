import pygame
import sys

SCREEN_W = 800
SCREEN_H = 800
SQUARE_SIZE = SCREEN_W // 8

class Piece:
    def __init__(self, color, kind):
        self.color = color
        self.kind = kind

    def __str__(self):
        return f"{self.color}{self.kind}"

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
    def __init__(self, piece_imgs, start_pos):
        self.grid = start_pos 
        self.piece_imgs = piece_imgs

    def handle_input(self, e):
        pass

    def update(self):
        pass

    def draw(self, screen):
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col:
                    screen.blit(self.piece_imgs[str(col)], (j*SQUARE_SIZE, i*SQUARE_SIZE))

def main():
    pygame.init()
    clock = pygame.time.Clock()

    unscaled_icon = pygame.image.load("assets/icon.png")
    scaled_icon = pygame.transform.scale(unscaled_icon, (32,32))
    pygame.display.set_icon(scaled_icon)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.SCALED, vsync=1)
    pygame.display.set_caption("P2 Chess")

    board_img = pygame.image.load("assets/board.svg")
    board_img = pygame.transform.scale(board_img, (SCREEN_W, SCREEN_H))

    piece_initials = ["R","N","B","Q","K","P"] 
    colors = ["b","w"]
    piece_imgs = {}
    for initial in piece_initials:
        for color in colors:
            piece = f"{color}{initial}"
            piece_img = pygame.image.load(f"assets/pieces/{piece}.svg")
            scaled_img = pygame.transform.scale(piece_img, (SQUARE_SIZE, SQUARE_SIZE))
            piece_imgs[piece] = scaled_img

    board = Board(piece_imgs, DEFAULT_START_POS)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
            board.handle_input(e)
        screen.blit(board_img, (0,0))
        board.update()
        board.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

