import pygame
import os


def load_hangman_images():
    """Load all hangman stage images."""
    images = []
    base_path = os.path.dirname(__file__)

    for i in range(7):
        image_path = os.path.join(base_path, "imgs", f"hangman{i}.png")
        image = pygame.image.load(image_path)
        images.append(image)

    return images


def blit_text_center(win, font, text, y_offset=0, color=(0, 0, 0)):
    """Blit text centered on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(
        center=(win.get_width() // 2, win.get_height() // 2 + y_offset)
    )
    win.blit(text_surface, text_rect)
    return text_rect


def setup_letter_buttons():
    """Setup letter button positions."""
    from .constants import WIDTH, RADIUS, GAP

    letters = []
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 400
    A = 65

    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])

    return letters
