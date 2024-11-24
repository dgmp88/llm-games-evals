from dataclasses import dataclass, field
from datetime import datetime
import pickle

import chess
from game import env
from game.game import Game
from game.players.llm_player import LLMPlayer
from game.players.stockfish_player import StockfishPlayer
from game.types import LLMModel, Outcome


@dataclass
class Result:
    outcome: Outcome
    moves: list[chess.Move]
    time_taken_s: float
    white: str
    black: str
    llm: str
    stockfish_elo: int
    timestamp: datetime = field(default_factory=datetime.now)

    def save(self):
        now_str = self.timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"result_{self.llm}_vs_stockfish_{self.stockfish_elo}_{now_str}.txt"

        file = env.RESULTS_DIR / filename

        with open(file, "wb") as f:
            pickle.dump(self, f)


def evaluate(model: LLMModel):
    for elo in [500, 800, 1000, 1500, 2000, 2500]:
        print(f"Evaluating model {model} against Stockfish {elo}")
        llm = LLMPlayer(model, debug=True)

        sf = StockfishPlayer(elo)
        game = Game(llm, sf, white=llm)

        outcome = game.play()

        result = Result(
            outcome=outcome,
            time_taken_s=game.game_time,
            moves=game.board.move_stack,
            stockfish_elo=elo,
            white=game.white.name,
            black=game.black.name,
            llm=llm.name,
        )

        result.save()

        if outcome.winner_name != llm.name:
            print(f"Stopped, didn't win against Stockfish {elo}")

            return


if __name__ == "__main__":
    models: list[LLMModel] = [
        "gpt-4o-mini-2024-07-18",
        # "gpt-4o-2024-08-06",
        # "claude-3-5-haiku-20241022",
        # "claude-3-5-sonnet-20241022",
    ]

    for model in models:
        evaluate(model)
