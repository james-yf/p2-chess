from board import Board

class GameState:
    def handle_input(self, e): pass
    def update(self): pass
    def draw(self, screen): pass

class PlayState(GameState):
    def __init__(self, assets, start_pos):
        self.board = Board(assets.board_img, assets.piece_imgs, start_pos)

    def handle_input(self, e):
        self.board.handle_input(e)

    def update(self):
        self.board.update()

    def draw(self, screen):
        self.board.draw(screen)
