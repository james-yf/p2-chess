import pygame
import time
import sys

SCREEN_W = 800
SCREEN_H = 800
SQUARE_SIZE = SCREEN_W // 8

BOARD = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], 
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"] 
]

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

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break

        screen.blit(board_img, (0,0))

        for i, row in enumerate(BOARD):
            for j, col in enumerate(row):
                if col:
                    screen.blit(piece_imgs[col], (j*SQUARE_SIZE, i*SQUARE_SIZE))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
