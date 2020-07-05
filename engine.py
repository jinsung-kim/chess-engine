import math
import random

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
    return math.floor(f * 10 ** n / 10 ** n)

class Board():
    def __init__(self):
        # The first letter represents the color of the piece 'b' or 'w'
        # The second letter represents the piece
        self.board = [
            # "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"
            # "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"
            ["bP", "bP", "bP", "--", "--", "wR", "--", "bK"],
            ["--", "--", "--", "--", "--", "wN", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "bN", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.last = None
        self.move_log = []
        # Used for checking for check, checkmate, and stalemates
        self.bK_pos = (4, 0)
        self.wK_pos = (4, 7)

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
            if (pos_x == moves[i][2] and pos_y == moves[i][3]):
                valid = True
                break

        if (valid):
            if (self.board[prev_y][prev_x] == "wP" and pos_y == 0): # pawn promotion
                self.move_log.append("wQ" + labels[pos_x] + str(8 - pos_y))
                self.board[pos_y][pos_x] = "wQ"
            else: # not pawn promotion
                if (self.board[prev_y][prev_x] == "wK"):
                    self.wK_pos = (pos_x, pos_y)
                self.move_log.append(self.board[prev_y][prev_x] + labels[pos_x] + str(8 - pos_y))
                self.board[pos_y][pos_x] = self.board[prev_y][prev_x]
            self.board[prev_y][prev_x] = "--"
            return True
        return False

    def make_ai_move(self):
        try:
            moves = self.get_all_moves("b")
            rand = random.randint(0, len(moves))
            if (rand == len(moves)):
                rand = 0
            rand = moves[rand]
            if (self.board[rand[1]][rand[0]] == "bP" and rand[3] == 7): # pawn promotion
                self.board[rand[3]][rand[2]] = "bQ"
                self.move_log.append("bQ" + labels[rand[0]] + str(8 - rand[1]))
            else:
                if (self.board[rand[1]][rand[0]] == "bK"): # King was moved
                    self.bK_pos = (rand[2], rand[3])
                self.board[rand[3]][rand[2]] = self.board[rand[1]][rand[0]]
                self.move_log.append(self.board[rand[3]][rand[2]] + \
                                    labels[rand[0]] + str(8 - rand[1]))
            self.board[rand[1]][rand[0]] = "--"
            print(self.look_for_checkmate("b")) # currently testing
        except IndexError:
            print("Black has no playable moves")
            print(self.move_log)

    def look_for_check(self, color):
        if (color == "b"):
            op = "w"
            pos = self.bK_pos
        else:
            op = "b"
            pos = self.wK_pos
        moves = self.get_all_moves(op) # gets all opposite move plays
        for i in range(len(moves)):
            if (pos[0] == moves[i][2] and pos[1] == moves[i][3]):
                return True
        return False

    # Checks if a position on the board is under attack
    # Used to check if a checkmate is valid (whether a king can move further)
    def under_attack(self, x, y, color):
        if (color == "b"):
            op = "w"
        else:
            op = "b"
        temp = self.board[y][x]
        self.board[y][x] = "--"
        moves = self.get_all_moves(op) # gets all opposite move plays after piece is removed
        self.board[y][x] = temp
        for i in range(len(moves)):
            if (x == moves[i][2] and y == moves[i][3]):
                return True
        return False

    def look_for_stalemate(self, color):
        pass

    def look_for_checkmate(self, color):
        '''
        1. Can I move out of mate?
        2. Can I block mate?
        3. Can I take the attacker?
        '''
        moves = []
        check_moves = {}
        attacking_pos = {}
        if (color == "b"):
            op = "w"
            pos = self.bK_pos
        else:
            op = "b"
            pos = self.wK_pos
        op_moves = self.get_all_moves(op) # gets all opposite move plays
        self.get_king_moves(pos[0], pos[1], moves, "b")
        # 1. King movement
        check_moves[pos] = 0 # current place of the king needs to be checked
        for i in range(len(moves)):
            check_moves[(moves[i][2], moves[i][3])] = 0
        for j in range(len(op_moves)):
            if (op_moves[j][2], op_moves[j][3]) in check_moves:
                check_moves[(op_moves[j][2], op_moves[j][3])] = 1
                attacking_pos[(op_moves[j][2], op_moves[j][3])] = 1
        print(check_moves.keys())
        print(check_moves.values())
        for move in check_moves:
            if (check_moves[move] == 0): # either safe or occupied by white piece
                # if occupied by white piece -> check if the spot will also be attacked
                print(move)
                attacked = self.under_attack(move[0], move[1], color)
                # if not, there is no checkmate
                if (not attacked):
                    return False
        # 2. King cannot move, look for a block
        block_counter = 0 # defend all of the spots needed (check_move length)
        defending_moves = self.get_all_moves(color) # all of the defending team's moves
        for move in defending_moves:
            curr = (move[2], move[3])
            if (curr in check_moves):
                if (pos == curr): # if king position is being attacked (game over)
                    return True
                elif (check_moves[curr] == 1): # needs to be defended
                    block_counter += 1
        # 3. Take out attackers
        # if there are multiple attacking positions, it is a checkmate
        if (len(attacking_pos) > 1):
            return True
        # precondition: there is only one piece threatening
        for move in defending_moves:
            curr = (move[2], move[3]) # current move
            if (curr in attacking_pos): # if the move can take out threatening piece
                return False
        return True

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
        if (color == "b"): # AI move
            if (y == 1): # hasn't moved yet (can move 1 or 2 forward)
                if (self.board[2][x] == "--"):
                    moves.append((x, y, x, 2))
                if (self.board[3][x] == "--" and self.board[2][x] == "--"):
                    moves.append((x, y, x, 3))
            else: # no double step available
                if (y == 7): # cannot progress anymore (when promoting -> shouldn't happen)
                    return 
                if (self.board[y + 1][x] == "--"): # move forward one
                    moves.append((x, y, x, y + 1))
                # diagonal attacks
                if (x == 0):
                    if ("w" in self.board[y + 1][1]):
                        moves.append((x, y, 1, y + 1))
                elif (x == 7):
                    if ("w" in self.board[y + 1][6]):
                        moves.append((x, y, 6, y + 1))
                else:
                    if ("w" in self.board[y + 1][x + 1]):
                        moves.append((x, y, x + 1, y + 1))
                    if ("w" in self.board[y + 1][x - 1]):
                        moves.append((x, y, x - 1, y + 1))
        else: # color is white
            if (y == 6): # hasn't moved yet (can move 1 or 2 forward)
                if (self.board[5][x] == "--"):
                    moves.append((x, y, x, 5))
                if (self.board[4][x] == "--"  and self.board[5][x] == "--"):
                    moves.append((x, y, x, 4))
            else: # no double step available
                if (y == 0): # cannot progress anymore (when promoting -> shouldn't happen)
                    return 
                if (self.board[y - 1][x] == "--"): # move forward one
                    moves.append((x, y, x, y - 1))
                # diagonal attacks
                if (x == 0):
                    if ("b" in self.board[y - 1][1]):
                        moves.append((x, y, 1, y - 1))
                elif (x == 7):
                    if ("b" in self.board[y - 1][6]):
                        moves.append((x, y, 6, y - 1))
                else:
                    if ("b" in self.board[y - 1][x + 1]):
                        moves.append((x, y, x + 1, y - 1))
                    if ("b" in self.board[y - 1][x - 1]):
                        moves.append((x, y, x - 1, y - 1))

    def get_rook_moves(self, x, y, moves, color):
        if (color == "b"): # gets opposite color
            op = "w"
        else:
            op = "b"
        # horizontal moves
        for i in range(x - 1, -1, -1):
            if (self.board[y][i] == "--"):
                moves.append((x, y, i, y))
            elif (op in self.board[y][i]):
                moves.append((x, y, i, y))
                break
            else:
                break
        for i in range(x + 1, 8):
            if (self.board[y][i] == "--"):
                moves.append((x, y, i, y))
            elif (op in self.board[y][i]):
                moves.append((x, y, i, y))
                break
            else:
                break
        # vertical moves
        for i in range(y - 1, -1, -1):
            if (self.board[i][x] == "--"):
                moves.append((x, y, x, i))
            elif (op in self.board[i][x]):
                moves.append((x, y, x, i))
                break
            else:
                break
        for i in range(y + 1, 8):
            if (self.board[i][x] == "--"):
                moves.append((x, y, x, i))
            elif (op in self.board[i][x]):
                moves.append((x, y, x, i))
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
                    moves.append((x, y, n_x, n_y))

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
                moves.append((x, y, i, j))
            elif (op in self.board[j][i]):
                moves.append((x, y, i, j))
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
                moves.append((x, y, i, j))
            elif (op in self.board[j][i]):
                moves.append((x, y, i, j))
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
                moves.append((x, y, i, j))
            elif (op in self.board[j][i]):
                moves.append((x, y, i, j))
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
                moves.append((x, y, i, j))
            elif (op in self.board[j][i]):
                moves.append((x, y, i, j))
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
                moves.append((x, y, x - 1, y))
            if (y > 0):
                if (op in self.board[y - 1][x - 1] or self.board[y - 1][x - 1] == "--"):
                    moves.append((x, y, x - 1, y - 1))
            if (y < 7):
                if (op in self.board[y + 1][x - 1] or self.board[y + 1][x - 1] == "--"):
                    moves.append((x, y, x - 1, y + 1))
        if (y > 0):
            if (op in self.board[y - 1][x] or self.board[y - 1][x] == "--"):
                moves.append((x, y, x, y - 1))
            if (x < 7):
                if (op in self.board[y - 1][x + 1] or self.board[y - 1][x + 1] == "--"):
                    moves.append((x, y, x + 1, y - 1))
        if (x < 7):
            if (op in self.board[y][x + 1] or self.board[y][x + 1] == "--"):
                moves.append((x, y, x + 1, y))
            if (y < 7):
                if (op in self.board[y + 1][x + 1] or self.board[y + 1][x + 1] == "--"):
                    moves.append((x, y, x + 1, y + 1))
        if (y < 7):
            if (op in self.board[y + 1][x] or self.board[y + 1][x] == "--"):
                moves.append((x, y, x, y + 1))
