from unittest import TestCase

from game.game import Game
from game.players.stockfish_player import StockfishPlayer


class TestGame(TestCase):

    def test_one_game(self):
        time_limit_ms = 100
        p1 = StockfishPlayer(elo=2000, time_limit_ms=time_limit_ms)
        p2 = StockfishPlayer(elo=1000, time_limit_ms=time_limit_ms)

        game = Game(p1, p2)
        game.play()
        outcome = game.board.outcome()

        self.assertEqual(outcome.termination.name, "CHECKMATE")
        self.assertEqual(
            game.get_winner().name, "stockfish_2000", "Strong player should win"
        )

        game.print_game_time()

        sf_thinking_time = sum(p1.sf_thinking_times) + sum(p2.sf_thinking_times)
        print(f"Stockfish thinking time: {sf_thinking_time:.2f} seconds")

    def test_ten_games(self):
        time_limit_ms = 100
        n_games = 10
        strong_wins = 0

        for i in range(n_games):
            print(".")
            p1 = StockfishPlayer(elo=1200, time_limit_ms=time_limit_ms)
            p2 = StockfishPlayer(elo=1000, time_limit_ms=time_limit_ms)

            game = Game(p1, p2)
            game.play()

            strong_won = game.get_winner().name == "strong"
            if strong_won:
                strong_wins += 1

        print(f"Strong player won {strong_wins} out of {n_games} games")
