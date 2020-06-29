import pygame
import time
import math
from board import Board

DISPLAY_HEIGHT = 400
DISPLAY_WIDTH = 400
SQUARE_SIDE = 50
"""
1 for only defending 
2 for defending and attacking possible trades
3 recommended for competitive AI
"""
AI_SEARCH_DEPTH = 2

RED_CHECK = (240, 150, 150)
YELLOW = (255,255,0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_LIGHT = (140, 184, 219)
BLUE_DARK = (91,  131, 159)
GRAY_LIGHT = (240, 240, 240)
GRAY_DARK = (200, 200, 200)
BROWN = (160,82,45)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
game_board = Board()

bB = pygame.image.load("assets/bB.png")
bK = pygame.image.load("assets/bK.png")
bN = pygame.image.load("assets/bN.png")
bP = pygame.image.load("assets/bP.png")
bQ = pygame.image.load("assets/bQ.png")
bR = pygame.image.load("assets/bR.png")

wB = pygame.image.load("assets/wB.png")
wK = pygame.image.load("assets/wK.png")
wN = pygame.image.load("assets/wN.png")
wP = pygame.image.load("assets/wP.png")
wQ = pygame.image.load("assets/wQ.png")
wR = pygame.image.load("assets/wR.png")

image_dict = {
    "bB": bB,
    "bK": bK,
    "bN": bN,
    "bP": bP,
    "bQ": bQ,
    "bR": bR,
    "wB": wB,
    "wK": wK,
    "wN": wN,
    "wP": wP,
    "wQ": wQ,
    "wR": wR
}

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


def draw_square(pos_x, pos_y, color):
    pygame.draw.rect(game_display, color, pygame.Rect(pos_x, pos_y, SQUARE_SIDE, SQUARE_SIDE))


def draw_board():
    game_display.fill(BROWN)
    for i in range(4):
        for j in range(4):
            draw_square(i * 100, j * 100, WHITE)
            draw_square((i * 100) + 50, (j * 100) + 50, WHITE)


def highlight_board(x, y):
    # Position on board
    pos_x = int(truncate(x / 50, 0))
    pos_y = int(truncate(y / 50, 0))
    # Current piece clicked on
    draw_square(pos_x * 50, pos_y * 50, YELLOW)

    # Places that current piece can go
    # If the piece is empty or belongs to the black side, do nothing
    possible_combos = []
    piece = game_board.board[pos_y][pos_x]
    if (piece == "wN"): # Knight (l shaped)
        highlight_knight(pos_x, pos_y)
    elif (piece == "wR"): # Rook (vertical and horizontal)
        highlight_rook(pos_x, pos_y)
    elif (piece == "wB"): # Bishop (diagonal)
        # i = pos_x - 1
        # j = pos_y - 1
        # while (i >= 0 and j >= 0):
        #     if ("w" in game_board.board[i][j]):
        #         break
        #     else:
        #         draw_square(i * 50, j * 50, YELLOW)
        #         if ("b" in game_board.board[i][pos_x]):
        #             break
        # while (i >= 0 and j <= 7):
        #     pass
        # while (i <= 7 and j >= 0):
        #     pass
        # while (i <= 7 and j <= 7):
        #     pass
        pass


def highlight_knight(pos_x, pos_y):
    possible_combos = [(pos_x - 2, pos_y + 1), (pos_x - 2, pos_y - 1), \
                        (pos_x - 1, pos_y - 2), (pos_x + 1, pos_y - 2), \
                        (pos_x + 2, pos_y - 1), (pos_x + 2, pos_y + 1), \
                        (pos_x + 1, pos_y + 2), (pos_x - 1, pos_y + 2)]

    for i in range(len(possible_combos)):
        curr_x = possible_combos[i][0]
        curr_y = possible_combos[i][1]
        if (curr_x >= 0 and curr_x <= 7 and curr_y >= 0 and curr_y <= 7):
            if ("b" in game_board.board[curr_y][curr_x]):
                draw_square(curr_x * 50, curr_y * 50, BLUE_LIGHT)
            elif ("w" not in game_board.board[curr_y][curr_x]):
                draw_square(curr_x * 50, curr_y * 50, YELLOW)


def highlight_rook(pos_x, pos_y):
    up_count = pos_y - 1
    down_count = pos_y + 1
    left_count = pos_x - 1
    right_count = pos_x + 1
    for i in range(up_count, -1, -1):
        if ("w" in game_board.board[i][pos_x]):
            break
        else:
            if ("b" in game_board.board[i][pos_x]):
                draw_square(pos_x * 50, i * 50, BLUE_LIGHT)
                break
            else:
                draw_square(pos_x * 50, i * 50, YELLOW)
    for i in range(down_count, 8):
        if ("w" in game_board.board[i][pos_x]):
            break
        else:
            if ("b" in game_board.board[i][pos_x]):
                draw_square(pos_x * 50, i * 50, BLUE_LIGHT)
                break
            else:
                draw_square(pos_x * 50, i * 50, YELLOW)
    for i in range(left_count, -1, -1):
        if ("w" in game_board.board[pos_y][i]):
            break
        else:
            if ("b" in game_board.board[pos_y][i]):
                draw_square(i * 50, pos_y * 50, BLUE_LIGHT)
                break
            else:
                draw_square(i * 50, pos_y * 50, YELLOW)
    for i in range(right_count, 8):
        if ("w" in game_board.board[pos_y][i]):
            break
        else:
            if ("b" in game_board.board[pos_y][i]):
                draw_square(i * 50, pos_y * 50, BLUE_LIGHT)
                break
            else:
                draw_square(i * 50, pos_y * 50, YELLOW)


def draw_pieces():
    for x in range(8):
        for y in range(8):
            if (game_board.board[y][x] != "--"):
                game_display.blit(image_dict[game_board.board[y][x]], ((x * 50) - 5, (y * 50) - 5))

def main():
    pygame.init()
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    game_exit = False
    mouse_x_cor = -1
    mouse_y_cor = -1
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    mouse_cor = pygame.mouse.get_pos()
                    mouse_x_cor = mouse_cor[0]
                    mouse_y_cor = mouse_cor[1]

        draw_board()
        highlight_board(mouse_x_cor, mouse_y_cor)
        draw_pieces()
        pygame.display.update()

main()
pygame.quit()
quit()