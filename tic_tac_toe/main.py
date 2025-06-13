import sys
import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen dimensions
WIDTH, HEIGHT = 300, 300
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3

# Line widths
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
LINE_WIDTH = 5

# Game setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

board = np.zeros((BOARD_ROWS, BOARD_COLS))  # 0: empty, 1: player, 2: AI


def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(
            WIN, color, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH
        )
    for i in range(1, BOARD_COLS):
        pygame.draw.line(
            WIN, color, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH
        )


def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.line(
                    WIN,
                    color,
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE // 4,
                        row * SQUARE_SIZE + SQUARE_SIZE // 4,
                    ),
                    (
                        col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                        row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                    ),
                    CROSS_WIDTH,
                )
                pygame.draw.line(
                    WIN,
                    color,
                    (
                        col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                        row * SQUARE_SIZE + SQUARE_SIZE // 4,
                    ),
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE // 4,
                        row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                    ),
                    CROSS_WIDTH,
                )
            elif board[row][col] == 2:
                pygame.draw.circle(
                    WIN,
                    color,
                    (
                        int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                        int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    ),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH,
                )


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    return not np.any(board == 0)


def check_win(player, check_board=None):
    if check_board is None:
        check_board = board

    # Check rows and columns
    for i in range(3):
        if np.all(check_board[i, :] == player) or np.all(check_board[:, i] == player):
            return True
    # Diagonals
    if np.all(np.diag(check_board) == player) or np.all(
        np.diag(np.fliplr(check_board)) == player
    ):
        return True
    return False


def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return 1
    elif check_win(1, minimax_board):
        return -1
    elif np.all(minimax_board != 0):  # Board is full
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score


def best_move():
    best_score = -float("inf")
    move = (-1, -1)
    temp_board = board.copy()  # Create a copy to avoid modifying the original

    for row in range(3):
        for col in range(3):
            if temp_board[row][col] == 0:
                temp_board[row][col] = 2
                score = minimax(temp_board, 0, False)
                temp_board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False


def restart_game():
    global board, player, game_over, winner
    board = np.zeros((3, 3))
    player = 1
    game_over = False
    winner = None


# Initial draw
WIN.fill(BLACK)
draw_lines()

# Game state
player = 1
game_over = False
winner = None

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and player == 1:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                row = mouseY // SQUARE_SIZE
                col = mouseX // SQUARE_SIZE

                if available_square(row, col):
                    mark_square(row, col, 1)
                    if check_win(1):
                        game_over = True
                        winner = 1
                    elif is_board_full():
                        game_over = True
                        winner = 0
                    else:
                        player = 2

            if player == 2 and not game_over:
                if best_move():
                    if check_win(2):
                        game_over = True
                        winner = 2
                    elif is_board_full():
                        game_over = True
                        winner = 0
                player = 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()

    WIN.fill(BLACK)

    if game_over:
        if winner == 1:
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif winner == 2:
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)
    else:
        draw_figures()
        draw_lines()

    pygame.display.update()
    clock.tick(60)
