import pygame
import sys
from .constants import FPS
from .models.hangman_game import HangmanGame
from .models.hangman_ui import HangmanUI


class HangmanApp:
    def __init__(self):
        pygame.init()
        self.game = HangmanGame()
        self.ui = HangmanUI()
        self.running = True
        self.game_over_screen = False

    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif self.game_over_screen:
                    if event.key == pygame.K_SPACE:
                        self.start_new_game()

                else:
                    # Handle letter input
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        self.make_guess(letter)

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over_screen:
                # Handle mouse clicks on letter buttons
                clicked_letter = self.ui.get_clicked_letter(pygame.mouse.get_pos())
                if clicked_letter:
                    self.make_guess(clicked_letter)

    def make_guess(self, letter):
        """Make a guess and update game state."""
        if not self.game.is_game_over():
            self.game.guess_letter(letter)

            if self.game.is_game_over():
                self.game_over_screen = True

    def start_new_game(self):
        """Start a new game."""
        self.game.reset_game()
        self.ui.reset_letter_buttons()
        self.game_over_screen = False

    def update(self):
        """Update game state."""
        pass  # Game logic is handled in events

    def render(self):
        """Render the current game state."""
        if self.game_over_screen:
            self.ui.draw_game_over(self.game)
        else:
            self.ui.draw_game(self.game)

    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.update()
            self.render()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    app = HangmanApp()
    app.run()


if __name__ == "__main__":
    main()
