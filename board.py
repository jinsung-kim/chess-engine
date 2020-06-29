import math


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


class Board():
    def __init__(self):
        # The first letter represents the color of the piece 'b' or 'w'
        # The second letter represents the piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "wK", "--", "--", "--"],
            ["--", "--", "--", "wR", "--", "wN", "--", "--"],
            ["--", "bP", "--", "bK", "--", "--", "--", "wQ"],
            ["--", "--", "wP", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.last = None
        self.move_log = []

    def make_move(self, x, y):
        pos_x = int(truncate(x / 50, 0))
        pos_y = int(truncate(y / 50, 0))
        valid = False
        if (self.last != None):
            prev_x = int(truncate(self.last[0] / 50, 0))
            prev_y = int(truncate(self.last[1] / 50, 0))
            if (self.board[prev_y][prev_x] == "wP"):
                valid = self.valid_pawn_move(prev_x, prev_y, pos_x, pos_y)
            elif (self.board[prev_y][prev_x] == "wR"):
                valid = self.valid_rook_move(prev_x, prev_y, pos_x, pos_y)
            elif (self.board[prev_y][prev_x] == "wN"):
                valid = self.valid_knight_move(prev_x, prev_y, pos_x, pos_y)
            elif (self.board[prev_y][prev_x] == "wB"):
                valid = self.valid_bishop_move(prev_x, prev_y, pos_x, pos_y)
            elif (self.board[prev_y][prev_x] == "wQ"):
                valid = self.valid_queen_move(prev_x, prev_y, pos_x, pos_y)
            elif (self.board[prev_y][prev_x] == "wK"):
                valid = self.valid_king_move(prev_x, prev_y, pos_x, pos_y)

        if (valid):
            print('move is valid')

    def valid_pawn_move(self, p_x, p_y, to_x, to_y):
        print(p_x, p_y)
        print(to_x, to_y)
        if (p_y == 6): # first move ever for a pawn
            if ((p_y - to_y == 1 or p_y - to_y == 2) and (p_x == to_x)):
                if ("b" in self.board[to_y][to_x]): # can't go two forward if black is there
                    return False
                else: # if it isn't, it's a valid move
                    return True
            return False
        else:
            if ((p_y - to_y == 1) and (p_x == to_x)): # move forward one
                if ("b" in self.board[to_y][to_x]):
                    return False
                else:
                    return True
            else: # diagonal attack
                if ((p_y - to_y == 1) and abs(p_x - to_x) == 1):
                    if ("b" in self.board[to_y][to_x]): # diagonal attack valid
                        return True
                    else: # diagonal attack is not valid
                        return False
                else:
                    return False
        return False

    def valid_rook_move(self, r_x, r_y, to_x, to_y):
        pass

    def valid_knight_move(self, k_x, k_y, to_x, to_y):
        pass

    def valid_bishop_move(self, b_x, b_y, to_x, to_y):
        pass

    def valid_queen_move(self, q_x, q_y, to_x, to_y):
        pass

    def valid_king_move(self, k_x, k_y, to_x, to_y):
        pass


