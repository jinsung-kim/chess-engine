import pygame
import time
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


def setup_game():
    pygame.init()
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()


def draw_board():
    game_display.fill(BROWN)
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(game_display, WHITE, pygame.Rect(i * 100, j * 100, SQUARE_SIDE, SQUARE_SIDE))
            pygame.draw.rect(game_display, WHITE, pygame.Rect((i * 100) + 50, (j * 100) + 50, SQUARE_SIDE, SQUARE_SIDE))
    

def draw_pieces():
    for i in range(8):
        for j in range(8):
            if (game_board.board[j][i] != "--"):
                game_display.blit(image_dict[game_board.board[j][i]], ((i * 50) - 5, (j * 50) - 5))

def main():
    setup_game()
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                pygame.quit()
                quit()
        draw_board()
        draw_pieces()
        pygame.display.update()
        # pygame.display.flip()
        # clock.tick(1)

main()
