import pygame
from board import Board
from constants import SQUARE_SIZE

class GameState:
    def handle_input(self, e): pass
    def update(self): pass
    def draw(self, screen): pass

class PlayState(GameState):
    def __init__(self, assets, start_pos):
        self.board = Board(assets.board_img, assets.piece_imgs, start_pos)

    def handle_input(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            m_x, m_y = e.pos
            sq = (m_y // SQUARE_SIZE, m_x // SQUARE_SIZE)
            self.board.handle_click(sq)

    def draw(self, screen):
        self.board.draw(screen)
