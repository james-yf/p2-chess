import pygame 
from constants import SQUARE_SIZE

OVERLAY_COLOR = (0,255,0)

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
        self.selected_sq = None

    def piece_at(self, sq):
        if sq is None: 
            return None
        sq_row, sq_col = sq
        return self.grid[sq_row][sq_col]  

    def piece_kind_at(self, sq):
        if sq is None: 
            return None
        at_sq = self.piece_at(sq) 
        return None if at_sq is None else at_sq[1]

    def piece_color_at(self, sq):
        if sq is None: 
            return None
        at_sq = self.piece_at(sq) 
        return None if at_sq is None else at_sq[0]

    def is_sq_empty(self, sq):
        sq_row, sq_col = sq
        return not self.grid[sq_row][sq_col]

    def does_sq_exist(self, sq):
        sq_row, sq_col = sq
        return sq_row >= 0 and sq_row <= 7 and sq_col >= 0 and sq_col <= 7 

    def are_sqs_friendly(self, sq1, sq2):
        if sq1 is None or sq2 is None: 
            return False
        return self.piece_color_at(sq1)==self.piece_color_at(sq2)
    
    def add_off_to_sq(self, sq, off):
        sq_row, sq_col = sq
        off_row, off_col = off
        return (sq_row+off_row, sq_col+off_col) 

    def slide_moves(self, src_sq, offs):
        moves = []
        for off in offs:
            target = self.add_off_to_sq(src_sq, off)
            while self.does_sq_exist(target):
                if not self.is_sq_empty(target):
                    if self.are_sqs_friendly(src_sq, target):
                        break
                    else:
                        moves.append((src_sq, target))
                        break
                moves.append((src_sq, target))
                target = self.add_off_to_sq(target, off)
        return moves

    def step_moves(self, src_sq, offs):
        moves = []
        for off in offs:
            target = self.add_off_to_sq(src_sq, off)
            if self.does_sq_exist(target) and not self.are_sqs_friendly(src_sq, target):
                moves.append((src_sq, target))
        return moves

    def pawn_moves(self, src_sq):
        pwn_color = self.piece_color_at(src_sq)
        moves = []

        #move up 1?
        off_up_1 = (-1,0) if pwn_color == "w" else (1,0)
        target = self.add_off_to_sq(src_sq, off_up_1)
        if self.does_sq_exist(target) and self.is_sq_empty(target):
            moves.append((src_sq, target))
            #move up 2?
            start_row = 6 if pwn_color == "w" else 1
            if src_sq[0] == start_row: 
                off_up_2 = (-2,0) if pwn_color == "w" else (2,0)
                target = self.add_off_to_sq(src_sq, off_up_2)
                if self.does_sq_exist(target) and self.is_sq_empty(target): 
                    moves.append((src_sq, target))

        #capture to the left?
        off_cap_l = (-1,-1) if pwn_color == "w" else (1,1)
        target = self.add_off_to_sq(src_sq, off_cap_l)
        if self.does_sq_exist(target) and not self.is_sq_empty(target) and not self.are_sqs_friendly(src_sq, target):
            moves.append((src_sq, target))

        #capture to the right?
        off_cap_r = (-1,1) if pwn_color == "w" else (1,-1)
        target = self.add_off_to_sq(src_sq, off_cap_r)
        if self.does_sq_exist(target) and not self.is_sq_empty(target) and not self.are_sqs_friendly(src_sq, target):
            moves.append((src_sq, target))

        return moves

    #unfiltered because it may contain pseudo moves, i.e., moves that adhere to piece's movement rules e.g., knight=L shape
    #but are not allowed in the current position as they would expose the king to check. 
    def unfiltered_moves_for_piece_at(self, sq):
        if sq is None: 
            return []

        kind = self.piece_kind_at(sq)
        if kind is None:
            return []

        vert_and_horiz_offs = ((-1,0),(0,1),(1,0),(0,-1))
        diag_offs = ((-1,-1),(-1,1),(1,1),(1,-1))

        if kind == "R":
            return self.slide_moves(sq, vert_and_horiz_offs)
        elif kind == "N":
            return self.step_moves(sq, ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)))
        elif kind == "B":
            return self.slide_moves(sq, diag_offs)
        elif kind == "Q":
            return self.slide_moves(sq, vert_and_horiz_offs + diag_offs)
        elif kind == "K":
            return self.step_moves(sq, vert_and_horiz_offs + diag_offs)
        elif kind == "P":
            return self.pawn_moves(sq)

    def find_king(self, color):
        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if self.piece_kind_at((i,j)) == "K" and self.piece_color_at((i,j)) == color:
                    return (i,j)

    def is_in_check(self, color):
        king_sq = self.find_king(color)
        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if not self.are_sqs_friendly(king_sq, (i,j)): 
                    enemy_moves = self.unfiltered_moves_for_piece_at((i,j)) 
                    for em in enemy_moves:
                        if king_sq == em[1]:
                            return True
        return False
    
    def filter_moves(self, moves):
        if not moves: 
            return []

        start_sq = moves[0][0]
        color_at_start = self.piece_color_at(start_sq)
        piece_at_start = self.piece_at(start_sq)

        filtered_moves = [] 
        start_row, start_col = start_sq 
        for mv in moves:
            dest_sq = mv[1]
            dest_row, dest_col = dest_sq 
            piece_at_dest = self.piece_at(dest_sq)
            self.grid[dest_row][dest_col] = piece_at_start 
            self.grid[start_row][start_col] = None 

            if not self.is_in_check(color_at_start):
                filtered_moves.append(mv)

            self.grid[dest_row][dest_col] = piece_at_dest 
            self.grid[start_row][start_col] = piece_at_start 

        return filtered_moves 

    def legal_moves_for_piece_at(self, sq):
        unfiltered_moves = self.unfiltered_moves_for_piece_at(sq)
        if not unfiltered_moves: 
            return []
        return self.filter_moves(unfiltered_moves)

    def handle_click(self, clicked_sq):
        if clicked_sq == self.selected_sq or self.is_sq_empty(clicked_sq):
            self.selected_sq = None
            return
        self.selected_sq = clicked_sq

    def draw(self, screen):
        screen.blit(self.board_img, (0,0))

        if self.selected_sq:
            sq_row, sq_col = self.selected_sq
            pygame.draw.rect(screen, OVERLAY_COLOR, (sq_col*SQUARE_SIZE, sq_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if piece:
                    screen.blit(self.piece_imgs[piece], (j*SQUARE_SIZE, i*SQUARE_SIZE))

        if self.selected_sq:
            for mv in self.legal_moves_for_piece_at(self.selected_sq):
                dest_row, dest_col = mv[1]
                pygame.draw.circle(screen, OVERLAY_COLOR, (dest_col*SQUARE_SIZE+SQUARE_SIZE//2, dest_row*SQUARE_SIZE+SQUARE_SIZE//2), SQUARE_SIZE//4)
