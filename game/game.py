import random
import time

import chess
import chess.engine

from game.types import LostByInvalidMoves, Player, Outcome
from game.util import get_board_emoji


class Game:

    def __init__(self, p1: Player, p2: Player, white: Player | None = None):
        self.p1 = p1
        self.p2 = p2

        if white is None:
            p1_white = random.choice([True, False])

            self.white = p1 if p1_white else p2
            self.black = p2 if p1_white else p1
        else:
            self.white = white
            self.black = p2 if white == p1 else p1

        self.board = chess.Board()
        self.outcome = None
        self.move_times: list[float] = []

    def play(self, max_moves: float | None = 75) -> Outcome:
        game_start_time = time.perf_counter()
        self.outcome = self._play(max_moves)
        print()  # to flush the dots
        game_end_time = time.perf_counter()
        self.game_time = game_end_time - game_start_time
        return self.outcome

    def _play(self, max_moves: float | None = 75) -> Outcome:
        board = self.board

        move_idx: float = 0  # Half move counter

        while not board.is_game_over():
            dots = "." * int(move_idx * 2)
            print(dots, end="", flush=True)
            if max_moves is not None and move_idx >= max_moves:
                return Outcome(
                    termination="too_many_moves",
                    winner_name=None,
                )
            move_start_time = time.perf_counter()
            mover: Player = self.white if board.turn == chess.WHITE else self.black

            try:
                move = mover.get_move(board)
            except LostByInvalidMoves:
                other: Player = self.black if board.turn == chess.WHITE else self.white
                return Outcome(
                    termination="invalid_moves",
                    winner_name=other.name,
                )

            board.push(move)
            move_end_time = time.perf_counter()
            self.move_times.append(move_end_time - move_start_time)
            move_idx += 0.5

        outcome = self.board.outcome()
        if outcome is None:
            # This should never happen, but type checking
            raise ValueError("Game is not over")

        if outcome.termination == chess.Termination.CHECKMATE:
            winner = self.white if outcome.winner == chess.WHITE else self.black
            return Outcome(
                termination="checkmate",
                winner_name=winner.name,
            )
        elif outcome.termination == chess.Termination.STALEMATE:
            return Outcome(
                termination="stalemate",
                winner_name=None,
            )
        else:
            raise ValueError("Unexpected termination type")

    def print_outcome(self):
        print(self.outcome)

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


if __name__ == "__main__":
    board = chess.Board()
    print(board)
    emj = get_board_emoji(board)
    print(emj)
