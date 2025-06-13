"""Game logic for Hangman."""

import random


class HangmanGame:
    """Main game logic for Hangman."""

    def __init__(self):
        from ..constants import WORDS, MAX_WRONG_GUESSES

        self.WORDS = WORDS
        self.MAX_WRONG_GUESSES = MAX_WRONG_GUESSES
        self.reset_game()

    def reset_game(self):
        """Reset the game to initial state."""
        self.word = random.choice(self.WORDS).upper()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.won = False

    def guess_letter(self, letter):
        """Make a guess and update game state."""
        letter = letter.upper()

        if letter in self.guessed_letters:
            return False  # Already guessed

        self.guessed_letters.add(letter)

        if letter not in self.word:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.MAX_WRONG_GUESSES:
                self.game_over = True
                self.won = False

        # Check if won
        if all(letter in self.guessed_letters for letter in self.word):
            self.game_over = True
            self.won = True

        return True  # Valid guess

    def get_display_word(self):
        """Get the word with guessed letters revealed."""
        return " ".join(
            letter if letter in self.guessed_letters else "_" for letter in self.word
        )

    def is_game_over(self):
        """Check if the game is over."""
        return self.game_over

    def is_won(self):
        """Check if the player won."""
        return self.won

    def get_hangman_stage(self):
        """Get the current hangman drawing stage."""
        return self.wrong_guesses
