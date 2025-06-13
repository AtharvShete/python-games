import pygame
from .utils import load_hangman_images

pygame.font.init()

# Display settings
WIDTH = 800
HEIGHT = 500
FPS = 60

# Initialize display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Button settings
RADIUS = 20
GAP = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("comicsans", 70)
MESSAGE_FONT = pygame.font.SysFont("comicsans", 50)

# Load hangman images
HANGMAN_IMAGES = load_hangman_images()

# Game settings
MAX_WRONG_GUESSES = 6
WORDS = [
    "PYTHON",
    "PYGAME",
    "CODING",
    "PROGRAMMING",
    "COMPUTER",
    "KEYBOARD",
    "MOUSE",
    "SCREEN",
    "WINDOW",
    "FUNCTION",
    "VARIABLE",
    "LOOP",
    "CLASS",
    "OBJECT",
    "METHOD",
    "STRING",
    "INTEGER",
    "BOOLEAN",
    "LIST",
    "DICTIONARY",
    "ALGORITHM",
    "DEBUG",
    "COMPILE",
    "EXECUTE",
    "SYNTAX",
]
