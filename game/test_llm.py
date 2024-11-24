import random
from unittest import TestCase

from game.game import Game
from game.player import LLMPlayer, StockfishPlayer
from game.util import pgn_from_board


class TestLLM(TestCase):
    def test_model(self):
        model = "gpt-4o-mini-2024-07-18"
        model = "gpt-4o-2024-08-06"
        llm = LLMPlayer(model)

        sf = StockfishPlayer(800)
        game = Game(llm, sf)

        game.play()
        game.print_outcome()


def generate_samples_for_system_prompt():
    time_limit_ms = 500
    p1 = StockfishPlayer(elo=10000, time_limit_ms=time_limit_ms)
    p2 = StockfishPlayer(elo=2000, time_limit_ms=time_limit_ms)

    game = Game(p1, p2)
    max_moves: float = random.randint(3, 8)

    if random.choice([True, False]):
        max_moves += 0.5
    game.play(max_moves=max_moves)

    pgn_board = pgn_from_board(game.board)
    print(pgn_board)


if __name__ == "__main__":
    generate_samples_for_system_prompt()

    # llm = LLMPlayer("gpt-4o-mini-2024-07-18")
    # sf = StockfishPlayer("stockfish", 2000)
    # game = Game(llm, sf)

    # game.play()
