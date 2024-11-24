import random
import time

import chess
import chess.engine

from game.player import Player


class Game:
    def __init__(self, p1: Player, p2: Player):
        self.p1 = p1
        self.p2 = p2

        self.p1_white = random.choice([True, False])

        self.white = p1 if self.p1_white else p2
        self.black = p2 if self.p1_white else p1

        self.board = chess.Board()

    def play(self, max_moves: float | None = None):
        game_start_time = time.perf_counter()
        move_times: list[float] = []
        board = self.board

        move_idx: float = 0  # Half move counter

        while not board.is_game_over():
            if max_moves is not None and move_idx >= max_moves:
                break
            move_start_time = time.perf_counter()
            if board.turn == chess.WHITE:
                move = self.white.get_move(board)
            else:
                move = self.black.get_move(board)
            board.push(move)
            move_end_time = time.perf_counter()
            move_times.append(move_end_time - move_start_time)
            move_idx += 0.5

        game_end_time = time.perf_counter()
        self.game_time = game_end_time - game_start_time
        self.move_times = move_times

    def print_outcome(self):
        outcome = self.board.outcome()
        if outcome is None:
            raise ValueError("Game is not over")

        print(f"Termination type: {outcome.termination.name}")

        if outcome.winner is None:
            print("Game is a draw")
        else:
            winning_player = self.white if outcome.winner == chess.WHITE else self.black
            print(f"Winning player: {winning_player.name}")

    def get_winner(self) -> Player | None:
        outcome = self.board.outcome()
        if outcome is None or outcome.winner is None:
            return None
        else:
            return self.white if outcome.winner == chess.WHITE else self.black

    def print_game_time(self):
        print(f"Game time: {self.game_time:.2f} seconds")
        avg_move_time = sum(self.move_times) / len(self.move_times)
        print(
            f"Average move time: {avg_move_time:.2f} seconds over {len(self.move_times) / 2} moves"
        )
