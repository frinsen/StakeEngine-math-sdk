"""Main file for generating crash game results - ported from Node.js game.js"""

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    num_threads = 20
    batching_size = 50000
    compression = True
    profiling = False

    num_sim_args = {
        "base": int(1e4),  # 10,000 simulations
    }

    run_conditions = {
        "run_sims": True,
        "run_optimization": False,
        "run_analysis": False,
        "upload_data": False,
    }

    config = GameConfig()
    gamestate = GameState(config)

    if run_conditions["run_sims"]:
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )
    generate_configs(gamestate)
