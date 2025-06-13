"""UI components for the Hangman game."""

import pygame
import math


class HangmanUI:
    """Handles all UI rendering for the game."""

    def __init__(self):
        from ..constants import (
            WIN,
            WIDTH,
            HEIGHT,
            RADIUS,
            WHITE,
            BLACK,
            RED,
            GREEN,
            GRAY,
            LETTER_FONT,
            WORD_FONT,
            TITLE_FONT,
            MESSAGE_FONT,
            HANGMAN_IMAGES,
        )
        from ..utils import setup_letter_buttons

        self.WIN = WIN
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.RADIUS = RADIUS
        self.WHITE = WHITE
        self.BLACK = BLACK
        self.RED = RED
        self.GREEN = GREEN
        self.GRAY = GRAY

        self.letter_font = LETTER_FONT
        self.word_font = WORD_FONT
        self.title_font = TITLE_FONT
        self.message_font = MESSAGE_FONT
        self.hangman_images = HANGMAN_IMAGES

        self.letters = setup_letter_buttons()

    def reset_letter_buttons(self):
        """Reset all letter buttons to visible."""
        for letter in self.letters:
            letter[3] = True

    def draw_game(self, game, show_instructions=True):
        """Draw the main game screen."""
        self.WIN.fill(self.WHITE)

        # Draw title
        title_text = self.title_font.render("DEVELOPER HANGMAN", 1, self.BLACK)
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, 50))
        self.WIN.blit(title_text, title_rect)

        # Draw instructions
        if show_instructions:
            instruction_text = self.letter_font.render(
                "Click letters or use keyboard to guess!", 1, self.GRAY
            )
            instruction_rect = instruction_text.get_rect(center=(self.WIDTH // 2, 100))
            self.WIN.blit(instruction_text, instruction_rect)

            quit_text = self.letter_font.render("Press ESC to quit", 1, self.GRAY)
            quit_rect = quit_text.get_rect(center=(self.WIDTH // 2, 130))
            self.WIN.blit(quit_text, quit_rect)

        # Draw word
        display_word = game.get_display_word()
        word_text = self.word_font.render(display_word, 1, self.BLACK)
        word_rect = word_text.get_rect(center=(self.WIDTH // 2, 220))
        self.WIN.blit(word_text, word_rect)

        # Draw letter buttons
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible and ltr not in game.guessed_letters:
                pygame.draw.circle(self.WIN, self.BLACK, (x, y), self.RADIUS, 3)
                text = self.letter_font.render(ltr, 1, self.BLACK)
                text_rect = text.get_rect(center=(x, y))
                self.WIN.blit(text, text_rect)
            elif ltr in game.guessed_letters:
                # Show guessed letters in different color
                color = self.GREEN if ltr in game.word else self.RED
                pygame.draw.circle(self.WIN, color, (x, y), self.RADIUS, 3)
                text = self.letter_font.render(ltr, 1, color)
                text_rect = text.get_rect(center=(x, y))
                self.WIN.blit(text, text_rect)

        # Draw hangman
        hangman_stage = min(game.get_hangman_stage(), len(self.hangman_images) - 1)
        self.WIN.blit(self.hangman_images[hangman_stage], (150, 150))

        pygame.display.update()

    def draw_game_over(self, game):
        """Draw game over screen."""
        self.WIN.fill(self.WHITE)

        # Draw result message
        if game.is_won():
            message = "🎉 YOU WON! 🎉"
            color = self.GREEN
        else:
            message = "💀 YOU LOST! 💀"
            color = self.RED

        message_text = self.message_font.render(message, 1, color)
        message_rect = message_text.get_rect(
            center=(self.WIDTH // 2, self.HEIGHT // 2 - 50)
        )
        self.WIN.blit(message_text, message_rect)

        # Show the word
        word_text = f"The word was: {game.word}"
        word_surface = self.word_font.render(word_text, 1, self.BLACK)
        word_rect = word_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.WIN.blit(word_surface, word_rect)

        # Instructions
        instruction_text = "Press SPACE to play again or ESC to quit"
        instruction_surface = self.letter_font.render(instruction_text, 1, self.GRAY)
        instruction_rect = instruction_surface.get_rect(
            center=(self.WIDTH // 2, self.HEIGHT // 2 + 80)
        )
        self.WIN.blit(instruction_surface, instruction_rect)

        pygame.display.update()

    def get_clicked_letter(self, mouse_pos):
        """Get the letter that was clicked, if any."""
        m_x, m_y = mouse_pos

        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                distance = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                if distance < self.RADIUS:
                    return ltr

        return None
