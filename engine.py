import math

labels = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h"
}

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
            ["--", "bP", "--", "bR", "--", "--", "--", "wQ"],
            ["--", "--", "wP", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.last = None
        self.move_log = []

    def make_move(self, x, y):
        pos_x = int(truncate(x / 50, 0))
        pos_y = int(truncate(y / 50, 0))
        prev_x = -1
        prev_y = -1
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
            self.move_log.append(self.board[prev_y][prev_x] + labels[pos_x] + str(8 - pos_y))
            self.board[pos_y][pos_x] = self.board[prev_y][prev_x]
            self.board[prev_y][prev_x] = "--"
            return True
        return False

    def make_ai_move(self):
        moves = self.get_all_moves("b")
        print(moves)

    def get_all_moves(self, color):
        moves = []
        for i in range(8):
            for j in range(8):
                if (color in self.board[j][i]):
                    if ("P" in self.board[j][i]):
                        # testing purposes
                        # self.get_pawn_moves(i, j, moves, color)
                        pass
                    elif ("R" in self.board[j][i]):
                        self.get_rook_moves(i, j, moves, color)
                    elif ("N" in self.board[j][i]):
                        self.get_knight_moves(i, j, moves, color)
                    elif ("B" in self.board[j][i]):
                        self.get_bishop_moves(i, j, moves, color)
                    elif ("Q" in self.board[j][i]):
                        self.get_queen_moves(i, j, moves, color)
                    elif ("K" in self.board[j][i]):
                        self.get_king_moves(i, j, moves, color)
        return moves

    def get_pawn_moves(self, x, y, moves, color):
        if (color == "b"):
            if (y == 1): # hasn't moved yet (can move 1 or 2 forward)
                if (self.board[3][x] == "--"):
                    moves.append((x, 3))
                if (self.board[2][x] == "--"):
                    moves.append((x, 2))
            else:
                if (y == 7): # cannot progress anymore (when promoting -> shouldn't happen)
                    return 
                if (self.board[y + 1][x] == "--"): # move forward one
                    moves.append((x, y + 1))
                # diagonal attacks
                if (x == 0):
                    if ("w" in self.board[y + 1][1]):
                        moves.append((1, y + 1))
                elif (x == 7):
                    if ("w" in self.board[y + 1][6]):
                        moves.append((6, y + 1))
                else:
                    if ("w" in self.board[y + 1][x + 1]):
                        moves.append((x + 1, y + 1))
                    if ("w" in self.board[y + 1][x - 1]):
                        moves.append((x - 1, y + 1))
        else:
            if (y == 6): # hasn't moved yet (can move 1 or 2 forward)
                if (self.board[4][x] == "--"):
                    moves.append((x, 4))
                if (self.board[5][x] == "--"):
                    moves.append((x, 5))
            else:
                if (y == 0): # cannot progress anymore (when promoting -> shouldn't happen)
                    return 
                if (self.board[y - 1][x] == "--"): # move forward one
                    moves.append((x, y - 1))
                # diagonal attacks
                if ("b" in x == 0):
                    if (self.board[y - 1][1]):
                        moves.append((1, y - 1))
                elif ("b" in x == 7):
                    if (self.board[y - 1][6]):
                        moves.append((6, y - 1))
                else:
                    if ("b" in self.board[y - 1][x + 1]):
                        moves.append((x + 1, y - 1))
                    if ("b" in self.board[y - 1][x - 1]):
                        moves.append((x - 1, y - 1))

    def valid_pawn_move(self, p_x, p_y, to_x, to_y): # next: consider pawn promotion
        if ("w" in self.board[to_y][to_x]): # if there is a white piece there, cannot go
            return False
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

    def get_rook_moves(self, x, y, moves, color):
        if (color == "b"): # gets opposite color
            op = "w"
        else:
            op = "b"
        # horizontal moves
        for i in range(x - 1, -1, -1):
            print(self.board[y][i])
            if (self.board[y][i] == "--"):
                moves.append((i, y))
            elif (op in self.board[y][i]):
                moves.append((i, y))
                break
            else:
                break
        for i in range(x + 1, 8):
            print(self.board[y][i])
            if (self.board[y][i] == "--"):
                moves.append((i, y))
            elif (op in self.board[y][i]):
                moves.append((i, y))
                break
            else:
                break
        # vertical moves
        for i in range(y - 1, -1, -1):
            print(self.board[i][x])
            if (self.board[i][x] == "--"):
                moves.append((x, i))
            elif (op in self.board[i][x]):
                moves.append((x, i))
                break
            else:
                break
        for i in range(y + 1, 8):
            print(self.board[i][x])
            if (self.board[i][x] == "--"):
                moves.append((x, i))
            elif (op in self.board[i][x]):
                moves.append((x, i))
                break
            else:
                break

    def valid_rook_move(self, r_x, r_y, to_x, to_y):
        if ("w" in self.board[to_y][to_x]): # if there is a white piece there, check if Q or K
            if (self.board[to_y][to_x] == "wQ"):
                pass
            elif (self.board[to_y][to_x] == "wK"):
                pass
            else: # not a castling combination
                return False # if there is something white there
        if ((r_x != to_x) and (r_y != to_y)): # diagonal move
            return False
        if (r_x == to_x): # vertical
            if (r_y > to_y):
                for i in range(r_y - 1, to_y, -1):
                    if (self.board[i][r_x] != "--"):
                        return False
            else:
                for i in range(r_y + 1, to_y):
                    if (self.board[i][r_x] != "--"):
                        return False
        if (r_y == to_y): # horizontal
            if (r_x > to_x):
                for i in range(r_x - 1, to_x, -1):
                    if (self.board[r_y][i] != "--"):
                        return False
            else:
                for i in range(r_x + 1, to_x):
                    if (self.board[r_y][i] != "--"):
                        return False
        return True

    def get_knight_moves(self, x, y, moves, color):
        pass

    def valid_knight_move(self, k_x, k_y, to_x, to_y):
        if ("w" in self.board[to_y][to_x]):
            return False
        possible_combos = [(k_x - 2, k_y + 1), (k_x - 2, k_y - 1), \
                        (k_x - 1, k_y - 2), (k_x + 1, k_y - 2), \
                        (k_x + 2, k_y - 1), (k_x + 2, k_y + 1), \
                        (k_x + 1, k_y + 2), (k_x - 1, k_y + 2)]
        for i in range(len(possible_combos)):
            if ((possible_combos[i][0]) == to_x and (possible_combos[i][1] == to_y)):
                return True
        return False

    def get_bishop_moves(self, x, y, moves, color):
        pass

    def valid_bishop_move(self, b_x, b_y, to_x, to_y):
        if ("w" in self.board[to_y][to_x]): # occupied already
            return False
        if (abs(b_x - to_x) != abs(b_y - to_y)): # Not a diagonal move
            return False
        if (b_x > to_x and b_y > to_y): # NW
            i = to_x + 1
            j = to_y + 1
            while (i != b_x):
                if (self.board[j][i] != "--"):
                    return False
                i += 1
                j += 1
        elif (b_x > to_x and b_y < to_y): # SW
            i = to_x + 1
            j = to_y - 1
            while (i != b_x):
                if (self.board[j][i] != "--"):
                    return False
                i += 1
                j -= 1
        elif (b_x < to_x and b_y > to_y): # NE
            i = b_x + 1
            j = b_y - 1
            while (i != to_x):
                if (self.board[j][i] != "--"):
                    return False
                i += 1
                j -= 1
        else: # SE
            i = b_x + 1
            j = b_y + 1
            while (i != to_x):
                if (self.board[j][i] != "--"):
                    return False
                i += 1
                j += 1
        return True

    def get_queen_moves(self, x, y, moves, color):
        pass

    def valid_queen_move(self, q_x, q_y, to_x, to_y):
        if (self.board[to_y][to_x] == "wR"): # if there is a white piece there, check if r
            pass # castling feature (add later)
        if ("w" in self.board[to_y][to_x]):
            return False
        rook_check = self.valid_rook_move(q_x, q_y, to_x, to_y)
        bishop_check = self.valid_bishop_move(q_x, q_y, to_x, to_y)
        return rook_check or bishop_check

    def get_king_moves(self, x, y, moves, color):
        pass

    def valid_king_move(self, k_x, k_y, to_x, to_y):
        # Make sure the king is not in check
        if (self.board[to_y][to_x] == "wR"): # if there is a white piece there, check if rook
            pass # castling feature (add later)
        if ("w" in self.board[to_y][to_x]): # not a castling combination
            return False
        if (abs(k_x - to_x) > 1 or abs(k_y - to_y) > 1):
            return False
        return True

