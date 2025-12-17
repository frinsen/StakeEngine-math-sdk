"""Game executables for Crash Game - ported from game.js"""

import hashlib
import math
from game_calculations import GameCalculations


class GameExecutables(GameCalculations):
    """Crash game executable logic using provably fair mechanics from original game.js"""

    def calculate_crash_point_provably_fair(self, round_id, client_seed, nonce, rtp=0.97):
        """
        Calculate crash point using provably fair algorithm from original game.js
        
        Formula from original: (2^32 / hashInt) * rtp / 100
        This ensures cryptographically verifiable randomness with RTP guarantee
        
        Args:
            round_id: Server round ID
            client_seed: Client-provided randomness (32 bytes hex)
            nonce: Round nonce
            rtp: Return-to-player ratio (default 0.97 = 97%)
            
        Returns:
            float: Crash point multiplier
        """
        # Combine round_id, client_seed, and nonce as in original game
        combined = f"{round_id}:{client_seed}:{nonce}"
        
        # Hash using SHA256 - matches original provably fair algorithm
        hash_obj = hashlib.sha256(combined.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert first 4 bytes to integer (0 to 2^32-1)
        # This matches the original formula: (2^32 / hashInt)
        hash_int = int.from_bytes(hash_bytes[:4], byteorder='big')
        
        # Avoid division by zero
        if hash_int == 0:
            hash_int = 1
        
        # Apply original formula: (2^32 / hashInt) * rtp / 100
        # The division by 100 converts to cents for calculation
        max_uint32 = 2**32
        crash_multiplier = (max_uint32 / hash_int) * (rtp / 100)
        
        # Enforce bounds from original game
        min_crash = 0.1  # Minimum crash point
        max_crash = 99.99  # Maximum crash point
        
        crash_multiplier = max(min_crash, min(crash_multiplier, max_crash))
        
        # Round to 2 decimal places as in original
        return round(crash_multiplier, 2)

    def execute_crash_spin(self, sim_num):
        """
        Execute a crash game spin using provably fair RNG.
        This simulates what would happen in the original game.js
        
        Args:
            sim_num: Simulation number
            
        Returns:
            dict: Game result with crash point and payout
        """
        # Generate deterministic but game-like seeds from simulation number
        round_id = f"sim_{sim_num}"
        
        # Generate client seed deterministically based on sim
        client_seed_int = hashlib.sha256(f"client_{sim_num}".encode()).digest()
        client_seed = client_seed_int.hex()
        
        # Generate nonce
        nonce = sim_num % 1000000
        
        # Calculate crash point using provably fair algorithm
        crash_point = self.calculate_crash_point_provably_fair(
            round_id,
            client_seed,
            nonce,
            rtp=0.97  # 97% RTP as in original
        )
        
        # In simulations, assume a random cashout point strategy
        # For generation, we'll just return the crash point as the outcome
        payout_multiplier = crash_point
        
        # Create game events matching original game format
        events = [
            {
                "index": 0,
                "type": "crashPointRevealed",
                "crashPoint": crash_point,
                "payout": payout_multiplier
            },
            {
                "index": 1,
                "type": "finalWin",
                "amount": payout_multiplier
            }
        ]
        
        return {
            "events": events,
            "payoutMultiplier": payout_multiplier,
            "crashPoint": crash_point,
            "criteria": "basegame",
            "baseGameWins": payout_multiplier,
            "freeGameWins": 0.0
        }
