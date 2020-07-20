import math
import random
import copy

# https://github.com/AnthonyASanchez/PythonChessAi/blob/master/AlphaBetaPruning.py

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

# value of each piece
pieces = {
    "P": 10,
    "R": 50,
    "N": 30,
    "B": 30,
    "Q": 90,
    "K": 900
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
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
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
        for move in moves:
            if (pos_x == move[2] and pos_y == move[3]):
                valid = True
                break

        if (valid):
            if (self.board[prev_y][prev_x] == "wP" and pos_y == 0): # pawn promotion
                # move on board
                self.board[pos_y][pos_x] = "wQ"
                self.board[prev_y][prev_x] = "--"
                if (self.look_for_check("w") == False):
                    self.move_log.append(self.board[pos_y][pos_x] + labels[pos_x] + str(8 - pos_y))
                    return True
                else: # the move will result in a check / does not protect a check
                    self.board[prev_y][prev_x] = self.board[pos_y][pos_x]
                    self.board[pos_y][pos_x] = "--"
                    return False
                self.move_log.append("wQ" + labels[pos_x] + str(8 - pos_y))
            else: # not pawn promotion
                if (self.board[prev_y][prev_x] == "wK"):
                    self.wK_pos = (pos_x, pos_y)
                # move on board
                self.board[pos_y][pos_x] = self.board[prev_y][prev_x]
                self.board[prev_y][prev_x] = "--"
                if (self.look_for_check("w") == False):
                    self.move_log.append(self.board[pos_y][pos_x] + labels[pos_x] + str(8 - pos_y))
                    return True
                else: # the move will result in a check / does not protect a check
                    self.board[prev_y][prev_x] = self.board[pos_y][pos_x]
                    self.board[pos_y][pos_x] = "--"
                    if (self.board[prev_y][prev_x] == "wK"):
                        self.wK_pos = (prev_x, prev_y)
                    return False
        return False

    def make_ai_move(self):
        try:
            moves = self.get_all_moves("b")
            rand = random.randint(0, len(moves)) # makes a random move
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
        except IndexError:
            print()

    # Minimax algorithm with alpha-beta pruning
    def minimax(self, depth, board, alpha, beta, maximizing):
        if (depth == 0):
            pass
        best_move = None
        if (maximizing):
            pass
        else:
            pass
        return best_move


    # evalutes the board given the position
    def evaluate(self, board):
        pass

    def look_for_check(self, color):
        if (color == "b"):
            op = "w"
            pos = self.bK_pos
        else:
            op = "b"
            pos = self.wK_pos
        moves = self.get_all_moves(op) # gets all opposite move plays
        for move in moves:
            if (pos[0] == move[2] and pos[1] == move[3]):
                return True
        return False

    # Checks if a position on the board is under attack
    # Used to check if a checkmate is valid (whether a king can move further)
    def under_attack(self, or_x, or_y, x, y, color):
        if (color == "b"):
            op = "w"
        else:
            op = "b"
        temp = self.board[y][x]
        or_piece = self.board[or_y][or_x]
        self.board[y][x] = "--"
        self.board[or_y][or_x] = "--"
        moves = self.get_all_moves(op) # gets all opposite move plays after piece is removed
        self.board[y][x] = temp
        self.board[or_y][or_x] = or_piece
        for move in moves:
            if (x == move[2] and y == move[3]):
                return True
        return False

    # bug if king is blocking an escape route and piece does not see that due to the block
    def look_for_stalemate(self, color):
        check_moves = {}
        king_moves = []
        if (self.look_for_check(color)): # if there is a check, cannot be a stalemate
            return False
        # check for all possible moves and see if the king is the only one
        if (color == "b"):
            op = "w"
            pos = self.bK_pos
        else:
            op = "b"
            pos = self.wK_pos
        all_moves = self.get_all_moves(color)
        op_moves = self.get_potential_moves(op) # gets all opposite move plays
        self.get_king_moves(pos[0], pos[1], king_moves, color)
        for move in op_moves: # all opposite moves added into moves
            check_moves[(move[2], move[3])] = 0 # insert
        for move in king_moves:
            if ((move[2], move[3]) not in check_moves): # king move (might) not be in danger
                if (self.under_attack(move[0], move[1], move[2], move[3], color) == False):
                    return False # return false because not a stalemate
        for move in all_moves:
            if ((move[0], move[1]) != (pos[0], pos[1])): # not a king move
                return False # means there is an alternate move to be made
        return True
        

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
        for move in moves:
            check_moves[(move[2], move[3])] = 0
        for j in range(len(op_moves)):
            if (op_moves[j][2], op_moves[j][3]) in check_moves:
                check_moves[(op_moves[j][2], op_moves[j][3])] = 1
                attacking_pos[(op_moves[j][2], op_moves[j][3])] = 1
        for move in check_moves:
            if (check_moves[move] == 0): # either safe or occupied by white piece
                # if occupied by white piece -> check if the spot will also be attacked
                attacked = self.under_attack(pos[0], pos[1], move[0], move[1], color)
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
    
    # Gets all potential moves + valid moves (pawn diagonal attacks)
    # used to find potential stalemates
    def get_potential_moves(self, color):
        moves = self.get_all_moves(color)
        # add potential diagonals (for pawns)
        if (color == "b"): # for black
            for x in range(8):
                for y in range(8):
                    if (self.board[y][x] == "bP"):
                        if (y != 7):
                            if (x == 0):
                                if ("b" not in self.board[y + 1][1]):
                                    moves.append((x, y, 1, y + 1))
                            elif (x == 7):
                                if ("b" not in self.board[y + 1][6]):
                                    moves.append((x, y, 6, y + 1))
                            else:
                                if ("b" not in self.board[y + 1][x + 1]):
                                    moves.append((x, y, x + 1, y + 1))
                                if ("b" not in self.board[y + 1][x - 1]):
                                    moves.append((x, y, x - 1, y + 1))
        else: # for white
            for x in range(8):
                for y in range(8):
                    if (self.board[y][x] == "wP"):
                        if (y != 0):
                            if (x == 0):
                                if ("w" not in self.board[y - 1][1]):
                                    moves.append((x, y, 1, y - 1))
                            elif (x == 7):
                                if ("w" not in self.board[y - 1][6]):
                                    moves.append((x, y, 6, y - 1))
                            else:
                                if ("w" not in self.board[y - 1][x + 1]):
                                    moves.append((x, y, x + 1, y - 1))
                                if ("w" not in self.board[y - 1][x - 1]):
                                    moves.append((x, y, x - 1, y - 1))
        return moves

    def get_pawn_moves(self, x, y, moves, color):
        if (color == "b"): # AI move
            if (y == 1): # hasn't moved yet (can move 1 or 2 forward)
                if (self.board[2][x] == "--"):
                    moves.append((x, y, x, 2))
                if (self.board[3][x] == "--" and self.board[2][x] == "--"):
                    moves.append((x, y, x, 3))
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
