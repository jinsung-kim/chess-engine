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
            ["--", "wN", "--", "--", "--", "--", "--", "--"],
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
        self.print_board(self.board)

    
    def print_board(self, board):
        '''
        Prints an ASCII board
        '''
        line = ""
        for x in range(8):
            for y in range(8):
                if (board[x][y] == "bK"):
                    line = line + u'\u265A' + " "
                elif (board[x][y] == "bQ"):
                    line = line + u'\u265B' + " "
                elif (board[x][y] == "bR"):
                    line = line + u'\u265C' + " "
                elif (board[x][y] == "bB"):
                    line = line + u'\u265D' + " "
                elif (board[x][y] == "bN"):
                    line = line + u'\u265E' + " "
                elif (board[x][y] == "bP"):
                    line = line + u'\u265F' + " "
                elif (board[x][y] == "wK"):
                    line = line + u'\u2654' + " "
                elif (board[x][y] == "wQ"):
                    line = line + u'\u2655' + " "
                elif (board[x][y] == "wR"):
                    line = line + u'\u2656' + " "
                elif (board[x][y] == "wB"):
                    line = line + u'\u2657' + " "
                elif (board[x][y] == "wN"):
                    line = line + u'\u2658' + " "
                elif (board[x][y] == "wP"):
                    line = line + u'\u2659' + " "
                else:
                    line = line + ". "
            print(line)
            line = ""

    def make_move(self, x, y):
        '''
        Makes a move based on the x and y coordinates of the mouse click
        Checks the previous values, and sees if a valid move has been made
        '''
        pos_x = int(truncate(x / 50, 0))
        pos_y = int(truncate(y / 50, 0))
        # placeholders for x,y values
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
        '''
        Makes the actual move that the AI determines is the best move, then makes that move
        Note: The deeper the depth selected, the more powerful the AI will become as it looks further
        '''
        try:
            move = self.generate_best_ai_move(3, copy.deepcopy(self.board), True) # creates a separate board
            if (self.board[move[1]][move[0]] == "bP" and move[3] == 7): # pawn promotion
                self.board[move[3]][move[2]] = "bQ"
                self.move_log.append("bQ" + labels[move[0]] + str(8 - move[1]))
            else:
                if (self.board[move[1]][move[0]] == "bK"): # King was moved
                    self.bK_pos = (move[2], move[3])
                self.board[move[3]][move[2]] = self.board[move[1]][move[0]]
                self.move_log.append(self.board[move[3]][move[2]] + \
                                    labels[move[0]] + str(8 - move[1]))
            self.board[move[1]][move[0]] = "--"
        except IndexError:
            print()

    
    def generate_best_ai_move(self, depth, board, maximizing):
        '''
        This function looks for the most negative value and accompanying move
        Note: The more negative a move is evaluated, the better it is for the AI,
        because the evaluation is positive for user pieces, and negative for the AI
        '''
        possible_moves = self.alpha_beta_moves(board, "b") # all AI moves
        best_move_val = 9999
        best_move = None
        promotion_move = False
        for move in possible_moves:
            # make move
            board[move[3]][move[2]] = board[move[1]][move[0]]
            board[move[1]][move[0]] = "--"
            if (board[move[3]][move[2]][1] == "P" and move[3] == 7): # pawn promotion
                board[move[3]][move[2]] = "bQ"
                promotion_move = True
            
            val = min(best_move_val, self.minimax(depth - 1, board, -10000, 10000, not maximizing))

            # undo move
            board[move[1]][move[0]] = board[move[3]][move[2]]
            board[move[3]][move[2]] = "--"
            if (promotion_move): # pawn (de)motion
                board[move[1]][move[0]] = "bP"
                promotion_move = False

            if (val < best_move_val):
                best_move_val = val
                best_move = move
                print("Best score:", str(val))
                print("Best move:", move)
        return best_move


    def minimax(self, depth, board, alpha, beta, maximizing):
        '''
        The actual minimax algorithm with alpha-beta pruning
        If the max or min is not within range, then the branch 
        will no longer search within that branch
        '''
        if (depth == 0): # no further to go, evaluate the position of the board
            return -self.evaluate(board)
        promotion_move = False
        if (maximizing):
            best_move = -9999
            possible_moves = self.alpha_beta_moves(board, "w")
            for move in possible_moves:
                # makes the move
                board[move[3]][move[2]] = board[move[1]][move[0]]
                board[move[1]][move[0]] = "--"
                if (board[move[3]][move[2]][1] == "P" and move[3] == 0): # pawn promotion
                    board[move[3]][move[2]] = "wQ"
                    promotion_move = True
                # recursive call
                best_move = max(best_move, self.minimax(depth - 1, board, alpha, beta, not maximizing))
                # undo the move
                board[move[1]][move[0]] = board[move[3]][move[2]]
                board[move[3]][move[2]] = "--"
                if (promotion_move): # pawn (de)motion
                    board[move[1]][move[0]] = "wP"
                    promotion_move = False
                alpha = max(alpha, best_move)
                if (beta <= alpha): # no need to check branch further
                    return best_move
            return best_move
        else:
            best_move = 9999
            possible_moves = self.alpha_beta_moves(board, "b")
            for move in possible_moves:
                board[move[3]][move[2]] = board[move[1]][move[0]]
                board[move[1]][move[0]] = "--"
                if (board[move[3]][move[2]][1] == "P" and move[3] == 7): # pawn promotion
                    board[move[3]][move[2]] = "bQ"
                    promotion_move = True
                # recursive call
                best_move = min(best_move, self.minimax(depth - 1, board, alpha, beta, not maximizing))
                # undo the move
                board[move[1]][move[0]] = board[move[3]][move[2]]
                board[move[3]][move[2]] = "--"
                if (promotion_move): # pawn (de)motion
                    board[move[1]][move[0]] = "bP"
                    promotion_move = False
                beta = min(beta, best_move)
                if (beta <= alpha): # no need to check branch further
                    return best_move
            return best_move


    def evaluate(self, board):
        '''
        The provided board is evaluated with user pieces having a positive value, and negative for AI
        Ex: If the AI is up a knight, then the board will be evaluated at -30
        Ex: If the user is up a queen, then the board will be evaluated at +90
        Time Complexity: O(1) -> 64 pieces to be checked max, relies on dictionary
        '''
        val = 0
        for x in range(8):
            for y in range(8):
                # if the piece is your team's color, add its value
                if (self.board[x][y][0] == "w"):
                    val += pieces[self.board[x][y][1]]
                elif (self.board[x][y][0] == "b"): # deduct every time an opposite team piece is seen
                    val -= pieces[self.board[x][y][1]]
        return val
        

    def look_for_check(self, color):
        '''
        Looks for a check, given the current position of the king
        Time Complexity: O(n) -> Has to develop opponent moves to see if there is a risk
        '''
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


    def under_attack(self, or_x, or_y, x, y, color):
        '''
        Checks to see if a position on the board is under attack
        Used to check if a checkmate is valid (whether a king can move further)
        '''
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


    def look_for_stalemate(self, color):
        '''
        Checks to see if there is a current stalemate, in which the king cannot move
        Time Complexity: O(n) -> Looking for a check is linear, everything else is a simple comparison
        '''
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
        Looks for an end game situation by analyzing three cases:
        1. Can I move out of mate?
        2. Can I block mate?
        3. Can I take the attacker?
        Time Complexity: O(n) -> Looks for check and stalemate, which are linear
        '''
        moves = []
        check_moves = {}
        attacking_pos = {}
        king_attacked = 0
        if (color == "b"):
            op = "w"
            pos = self.bK_pos
        else:
            op = "b"
            pos = self.wK_pos
        op_moves = self.get_potential_moves(op) # gets all opposite move plays
        self.get_king_moves(pos[0], pos[1], moves, "b")
        # 1. King movement
        check_moves[pos] = 0 # current place of the king needs to be checked
        for move in moves:
            check_moves[(move[2], move[3])] = 0
        for move in op_moves:
            if (move[2], move[3]) in check_moves:
                check_moves[(move[2], move[3])] = 1
                if ((move[2], move[3]) in attacking_pos):
                    attacking_pos[(move[0], move[1])] += 1
                    # Note: If the king is attacked twice, checkmate
                    if (move[0] == pos[0] and move[1] == pos[1]):
                        king_attacked += 1
                else:
                    attacking_pos[(move[0], move[1])] = 1
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
        # if there are multiple attacking positions, it is a checkmate (by default)
        if (king_attacked > 1):
            return True
        # precondition: there is only one piece threatening
        for move in defending_moves:
            curr = (move[2], move[3]) # current move
            # if the move can take out threatening piece
            if (curr in attacking_pos):
                return False
        return True


    def alpha_beta_moves(self, board, color):
        '''
        Used to find potential moves (based on what the current state of the given board is)
        Returns the board to its original state
        '''
        moves = []
        temp_board = copy.deepcopy(self.board) # store the original board
        self.board = copy.deepcopy(board) # switch board
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
        # restore the original board
        self.board = temp_board
        return moves


    def get_all_moves(self, color):
        '''
        Gets all the real-time moves to be made for a team, 
        '''
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
    

    def get_potential_moves(self, color):
        '''
        Gets all the potential moves and valid moves
        Created to consider all pawn diagonal attacks that might lead to stalemates and checkmates
        '''
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
