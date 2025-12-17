"""Handles the state and output for a single crash game simulation round - ported from game.js"""

from game_override import GameStateOverride
from src.events.events import *


class GameState(GameStateOverride):
    """Handle game-logic and event updates for a crash game simulation.
    
    This implements the crash game logic from the original Node.js game.js:
    - Provably fair crash point calculation
    - Cash out logic
    - Payout calculation
    """

    def run_spin(self, sim, simulation_seed=None):
        """Execute a single crash game spin using original game.js logic."""
        self.reset_seed(sim)
        self.repeat = True
        
        while self.repeat:
            self.reset_book()

            # Execute crash game logic from original game.js
            result = self.execute_crash_spin(sim)
            
            # Add crash point reveal event (matching original game structure)
            game_event = {
                "index": len(self.book.events),
                "type": "crashPointRevealed",
                "crashPoint": result["crashPoint"],
                "payout": result["payoutMultiplier"]
            }
            self.book.add_event(game_event)
            
            # Update win data
            win_data = {"totalWin": result["payoutMultiplier"]}
            self.win_manager.update_spinwin(win_data["totalWin"])
            self.win_manager.update_gametype_wins(self.gametype)

            # Add final win event
            self.evaluate_finalwin()

        self.imprint_wins()

    def run_freespin(self):
        """Crash game has no free spins."""
        pass
