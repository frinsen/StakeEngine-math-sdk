"""Game state override for Crash Game."""

from game_executables import GameExecutables
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """Override universal state functions for crash game."""

    def reset_book(self):
        """Reset game specific properties"""
        super().reset_book()

    def assign_special_sym_function(self):
        pass

    def check_game_repeat(self):
        """Crash game doesn't repeat - one spin per round"""
        self.repeat = False
