import pygame 
from constants import SQUARE_SIZE

SELECTED_OVERLAY_COLOR = (0,255,0)
DRAW_OVERLAY_COLOR = (0,0,255)
MATE_OVERLAY_COLOR = (255,0,0)

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
        self.turn = "w"
        self.pwn_2_dest = None 
        self.result = None
        self.font = pygame.font.SysFont("Arial", 20)

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

    def piece_at_sq_has_color(self, sq, color):
        return self.piece_color_at(sq)==color

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
        
        #en passant
        if self.pwn_2_dest and src_sq[0] == self.pwn_2_dest[0]:
            off_en_col = self.pwn_2_dest[1] - src_sq[1]  
            if off_en_col == 1:
                off_cap_r = (-1,1) if pwn_color == "w" else (1,1)
                target = self.add_off_to_sq(src_sq, off_cap_l)
                moves.append((src_sq, target))
            else:
                off_cap_l = (-1,-1) if pwn_color == "w" else (1,-1)
                target = self.add_off_to_sq(src_sq, off_cap_l)
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

    def is_game_over(self):
        legal_moves = []
        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if self.piece_at_sq_has_color((i,j), self.turn): 
                    legal_moves += self.legal_moves_for_piece_at((i,j)) 
        if not legal_moves:
            if self.is_in_check(self.turn):
                self.result = "mate"
                return
            else:
                self.result = "draw"

    def is_move_pwn_2(self, move):
        start_sq, dest_sq = move 
        return self.piece_kind_at(start_sq) == "P" and (dest_sq[0] - start_sq[0]) in (2,-2)

    def is_move_en_passant(self, move):
        if self.pwn_2_dest is None: 
            return False

        src_sq, dest_sq = move
        if self.piece_kind_at(src_sq) != "P":
            return False

        src_col = src_sq[1]
        dest_row, dest_col = dest_sq
        pwn_2_row, pwn_2_col = self.pwn_2_dest

        return src_col != pwn_2_col and dest_row in (pwn_2_row - 1, pwn_2_row + 1) and dest_col == pwn_2_col

    def make_move(self, move):
        legal_moves = self.legal_moves_for_piece_at(move[0]) 
        if move in legal_moves:
            if self.is_move_en_passant(move):
                self.grid[self.pwn_2_dest[0]][self.pwn_2_dest[1]] = None
                self.pwn_2_dest = None

            if self.is_move_pwn_2(move):
                self.pwn_2_dest = move[1] 
            else:
                self.pwn_2_dest = None

            start_row, start_col = move[0]
            dest_row, dest_col = move[1]

            self.grid[dest_row][dest_col] = self.piece_at(move[0])
            self.grid[start_row][start_col] = None
            self.turn = "w" if self.turn == "b" else "b"

        if self.is_game_over(): 
            self.game_over = True 

    def handle_click(self, clicked_sq):
        if self.result:
            return
        if self.selected_sq == clicked_sq:
            self.selected_sq = None
            return
        if self.piece_at_sq_has_color(clicked_sq, self.turn): 
            self.selected_sq = clicked_sq
            return
        if self.selected_sq:
            self.make_move((self.selected_sq, clicked_sq)) 
            self.selected_sq = None

    def draw(self, screen):
        screen.blit(self.board_img, (0,0))

        if self.selected_sq:
            sq_row, sq_col = self.selected_sq
            pygame.draw.rect(screen, SELECTED_OVERLAY_COLOR, (sq_col*SQUARE_SIZE, sq_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        if self.result == "mate":
            loser_king_row, loser_king_col = self.find_king(self.turn)
            pygame.draw.rect(screen, MATE_OVERLAY_COLOR, (loser_king_col*SQUARE_SIZE, loser_king_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
        if self.result == "draw":
            curr_king_row, curr_king_col = self.find_king(self.turn)
            other_king_color = "b" if self.turn == "w" else "w" 
            other_king_row, other_king_col = self.find_king(other_king_color)
            pygame.draw.rect(screen, DRAW_OVERLAY_COLOR, (curr_king_col*SQUARE_SIZE, curr_king_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, DRAW_OVERLAY_COLOR, (other_king_col*SQUARE_SIZE, other_king_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if i == 7:
                    text_surface = self.font.render(f"{chr(ord('a')+j)}", True, (255, 0, 0))
                    screen.blit(text_surface, (j*SQUARE_SIZE+0.05*SQUARE_SIZE, i*SQUARE_SIZE+0.75*SQUARE_SIZE))
                if j == 7:
                    text_surface = self.font.render(f"{8-i}", True, (255, 0, 0))
                    screen.blit(text_surface, (j*SQUARE_SIZE+0.85*SQUARE_SIZE, i*SQUARE_SIZE))
                if piece:
                    screen.blit(self.piece_imgs[piece], (j*SQUARE_SIZE, i*SQUARE_SIZE))

        if self.selected_sq:
            for mv in self.legal_moves_for_piece_at(self.selected_sq):
                dest_row, dest_col = mv[1]
                pygame.draw.circle(screen, SELECTED_OVERLAY_COLOR, (dest_col*SQUARE_SIZE+SQUARE_SIZE//2, dest_row*SQUARE_SIZE+SQUARE_SIZE//2), SQUARE_SIZE//4)
