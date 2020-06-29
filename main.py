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

def draw_board():
    game_display.fill(BROWN)
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(game_display, WHITE, pygame.Rect(i * 100, j * 100, SQUARE_SIDE, SQUARE_SIDE))
            pygame.draw.rect(game_display, WHITE, pygame.Rect((i * 100) + 50, (j * 100) + 50, SQUARE_SIDE, SQUARE_SIDE))


def highlight_board(x, y):
    # Position on board
    pos_x = int(truncate(x / 50, 0))
    pos_y = int(truncate(y / 50, 0))
    # Current piece clicked on
    pygame.draw.rect(game_display, YELLOW, pygame.Rect(pos_x * 50, pos_y * 50, SQUARE_SIDE, SQUARE_SIDE))

    # Places that current piece can go
    # If the piece is empty or belongs to the black side, do nothing
    possible_combos = []
    piece = game_board.board[pos_y][pos_x]
    print(piece)
    if (piece == "wN"): # Knight
        print("Knight selected")
        possible_combos = [(pos_x - 2, pos_y + 1), (pos_x - 2, pos_y - 1), \
                            (pos_x - 1, pos_y - 2), (pos_x + 1, pos_y - 2), \
                            (pos_x + 2, pos_y - 1), (pos_x + 2, pos_y + 1), \
                            (pos_x + 1, pos_y + 2), (pos_x - 1, pos_y + 2)]

        for i in range(len(possible_combos)):
            curr_x = possible_combos[i][0]
            curr_y = possible_combos[i][1]
            if (curr_x >= 0 and curr_x <= 7 and curr_y >= 0 and curr_y <= 7):
                if ("w" not in game_board.board[curr_y][curr_x]):
                    print(game_board.board[curr_y][curr_x])
                    pygame.draw.rect(game_display, YELLOW, \
                    pygame.Rect(curr_x * 50, curr_y * 50, \
                    SQUARE_SIDE, SQUARE_SIDE))
    if (piece == "wR"): # Rook
        pass

        

def draw_pieces():
    for i in range(8):
        for j in range(8):
            if (game_board.board[j][i] != "--"):
                game_display.blit(image_dict[game_board.board[j][i]], ((i * 50) - 5, (j * 50) - 5))

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