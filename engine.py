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
            ["--", "bP", "--", "bB", "--", "--", "--", "wQ"],
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
        moves = []
        if (self.last != None):
            prev_x = int(truncate(self.last[0] / 50, 0))
            prev_y = int(truncate(self.last[1] / 50, 0))
            if (self.board[prev_y][prev_x] == "wP"):
                self.get_pawn_moves(prev_x, prev_y, moves, "w")
            elif (self.board[prev_y][prev_x] == "wR"):
                self.get_rook_moves(prev_x, prev_y, moves, "w")
            elif (self.board[prev_y][prev_x] == "wN"):
                self.get_knight_moves(prev_x, prev_y, moves, "w")
            elif (self.board[prev_y][prev_x] == "wB"):
                self.get_bishop_moves(prev_x, prev_y, moves, "w")
            elif (self.board[prev_y][prev_x] == "wQ"):
                self.get_rook_moves(prev_x, prev_y, moves, "w")
                self.get_bishop_moves(prev_x, prev_y, moves, "w")
            elif (self.board[prev_y][prev_x] == "wK"):
                self.get_king_moves(prev_x, prev_y, moves, "w")

        # Check if valid move
        for i in range(len(moves)):
            if (pos_x == moves[i][0] and pos_y == moves[i][1]):
                valid = True
                break

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
                        self.get_pawn_moves(i, j, moves, color)
                    elif ("R" in self.board[j][i]):
                        self.get_rook_moves(i, j, moves, color)
                    elif ("N" in self.board[j][i]):
                        self.get_knight_moves(i, j, moves, color)
                    elif ("B" in self.board[j][i]):
                        self.get_bishop_moves(i, j, moves, color)
                    elif ("Q" in self.board[j][i]):
                        self.get_bishop_moves(i, j, moves, color)
                        self.get_rook_moves(i, j, moves, color)
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

    def get_rook_moves(self, x, y, moves, color):
        if (color == "b"): # gets opposite color
            op = "w"
        else:
            op = "b"
        # horizontal moves
        for i in range(x - 1, -1, -1):
            if (self.board[y][i] == "--"):
                moves.append((i, y))
            elif (op in self.board[y][i]):
                moves.append((i, y))
                break
            else:
                break
        for i in range(x + 1, 8):
            if (self.board[y][i] == "--"):
                moves.append((i, y))
            elif (op in self.board[y][i]):
                moves.append((i, y))
                break
            else:
                break
        # vertical moves
        for i in range(y - 1, -1, -1):
            if (self.board[i][x] == "--"):
                moves.append((x, i))
            elif (op in self.board[i][x]):
                moves.append((x, i))
                break
            else:
                break
        for i in range(y + 1, 8):
            if (self.board[i][x] == "--"):
                moves.append((x, i))
            elif (op in self.board[i][x]):
                moves.append((x, i))
                break
            else:
                break

    def get_knight_moves(self, x, y, moves, color):
        possible_combos = [(x - 2, y + 1), (x - 2, y - 1), \
                        (x - 1, y - 2), (x + 1, y - 2), \
                        (x + 2, y - 1), (x + 2, y + 1), \
                        (x + 1, y + 2), (x - 1, y + 2)]
        for i in range(len(possible_combos)):
            n_x = possible_combos[i][0]
            n_y = possible_combos[i][1]
            if (n_x >= 0 and n_x <= 7 and n_y >= 0 and n_y <= 7):
                if (color not in self.board[n_y][n_x]):
                    moves.append((n_x, n_y))

    def get_bishop_moves(self, x, y, moves, color):
        if (color == "b"): # gets opposite color
            op = "w"
        else:
            op = "b"
        # SE
        i = x + 1
        j = y + 1
        while (i <= 7):
            if (j > 7):
                break
            if (self.board[j][i] == "--"):
                moves.append((i, j))
            elif (op in self.board[j][i]):
                moves.append((i, j))
                break
            else:
                break
            i += 1
            j += 1
        # NE
        i = x + 1
        j = y - 1
        while (i <= 7):
            if (j < 0):
                break
            if (self.board[j][i] == "--"):
                moves.append((i, j))
            elif (op in self.board[j][i]):
                moves.append((i, j))
                break
            else:
                break
            i += 1
            j -= 1
        # SW
        i = x - 1
        j = y + 1
        while (i >= 0):
            if (j > 7):
                break
            if (self.board[j][i] == "--"):
                moves.append((i, j))
            elif (op in self.board[j][i]):
                moves.append((i, j))
                break
            else:
                break
            i -= 1
            j += 1
        # NW
        i = x - 1
        j = y - 1
        while (i >= 0):
            if (j < 0):
                break
            if (self.board[j][i] == "--"):
                moves.append((i, j))
            elif (op in self.board[j][i]):
                moves.append((i, j))
                break
            else:
                break
            i -= 1
            j -= 1

    def get_king_moves(self, x, y, moves, color):
        if (color == "b"):
            op = "w"
        else:
            op = "b"
        if (x > 0):
            if (op in self.board[y][x - 1] or self.board[y][x - 1] == "--"):
                moves.append((x - 1, y))
            if (y > 0):
                if (op in self.board[y - 1][x - 1] or self.board[y - 1][x - 1] == "--"):
                    moves.append((x - 1, y - 1))
            if (y < 7):
                if (op in self.board[y + 1][x - 1] or self.board[y + 1][x - 1] == "--"):
                    moves.append((x - 1, y + 1))
        if (y > 0):
            if (op in self.board[y - 1][x] or self.board[y - 1][x] == "--"):
                moves.append((x, y - 1))
            if (x < 7):
                if (op in self.board[y - 1][x + 1] or self.board[y - 1][x + 1] == "--"):
                    moves.append((x + 1, y - 1))
        if (x < 7):
            if (op in self.board[y][x + 1] or self.board[y][x + 1] == "--"):
                moves.append((x + 1, y))
            if (y < 7):
                if (op in self.board[y + 1][x + 1] or self.board[y + 1][x + 1] == "--"):
                    moves.append((x + 1, y + 1))
        if (y < 7):
            if (op in self.board[y + 1][x] or self.board[y + 1][x] == "--"):
                moves.append((x, y + 1))
