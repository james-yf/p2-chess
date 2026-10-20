import pygame
import sys
from board import DEFAULT_START_POS
from states import PlayState
from constants import SCREEN_W, SCREEN_H
from assets import AssetManager

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.assets = AssetManager()
        self.assets.load_all()

        pygame.display.set_icon(self.assets.icon)

        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.SCALED, vsync=1)
        pygame.display.set_caption("P2 Chess")

        self.state = PlayState(self.assets, [row[:] for row in DEFAULT_START_POS])
        self.running = True

    def set_state(self, state):
        self.state = state 

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                    break
                self.state.handle_input(e)
            self.state.update()
            self.state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
