import time


import chess
from stockfish import Stockfish


from env import env
from game.types import Player


class StockfishPlayer(Player):
    def __init__(self, elo: int, depth: int = 10, time_limit_ms: int = 100):
        self.name = f"stockfish_{elo}"
        self.elo = elo
        self.time_limit_ms = time_limit_ms

        self.stockfish = Stockfish(path=env.STOCKFISH_PATH)
        self.stockfish.set_depth(depth)
        self.stockfish.set_elo_rating(elo)
        self.sf_thinking_times: list[float] = []

    def get_move(self, board: chess.Board) -> chess.Move:
        self.stockfish.set_position([move.uci() for move in board.move_stack])
        t0 = time.perf_counter()
        result = self.stockfish.get_best_move_time(self.time_limit_ms)

        t1 = time.perf_counter()
        self.sf_thinking_times.append(t1 - t0)

        if result is None:
            raise ValueError("Stockfish failed to return a move")
        move = chess.Move.from_uci(result)
        return move
