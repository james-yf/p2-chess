import pygame
import time
import sys

SCREEN_W = 800
SCREEN_H = 800

def main():
    pygame.init()
    clock = pygame.time.Clock()

    unscaled_icon = pygame.image.load("assets/icon.png")
    scaled_icon = pygame.transform.scale(unscaled_icon, (32,32))
    pygame.display.set_icon(scaled_icon)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("P2 Chess")

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
