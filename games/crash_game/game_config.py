"""Crash Game configuration - ported from original Node.js game.js"""

from src.config.config import Config
from src.config.distributions import Distribution
from src.config.config import BetMode


class GameConfig(Config):
    """Crash Game configuration with provably fair mechanics."""

    def __init__(self):
        super().__init__()
        self.game_id = "crash_game"
        self.provider_numer = 0
        self.working_name = "crash_game"
        self.wincap = 99.99  # Max multiplier
        self.win_type = "other"
        self.rtp = 0.97  # 97% RTP - matches original
        self.construct_paths()

        # Game Dimensions - No reels for crash game
        self.num_reels = 0
        self.num_rows = []
        self.paytable = {}
        self.include_padding = False
        self.special_symbols = {"wild": [], "scatter": [], "multiplier": []}

        self.freespin_triggers = {self.basegame_type: {}, self.freegame_type: {}}
        self.anticipation_triggers = {self.basegame_type: 0, self.freegame_type: 0}

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="basegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
        ]
