class Piece:
    def __init__(self, color, kind):
        self.color = color
        self.kind = kind
    def __str__(self):
        return f"{self.color}{self.kind}"
