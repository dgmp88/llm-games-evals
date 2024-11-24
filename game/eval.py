from dataclasses import dataclass, field
from datetime import datetime
import math
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
        filename = (
            f"result_{self.llm}_vs_stockfish_{self.stockfish_elo}_{now_str}.pickle"
        )

        file = env.RESULTS_DIR / filename

        with open(file, "wb") as f:
            pickle.dump(self, f)


def evaluate(model: LLMModel):
    for elo in [800, 1000, 1500, 2000, 2500]:
        print(f"Evaluating model {model} against Stockfish {elo}")
        llm = LLMPlayer(model)

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


def models():
    models: list[LLMModel] = [
        "gpt-4o-mini-2024-07-18",
        "gpt-4o-2024-08-06",
        "gpt-4o-2024-11-20",
        "claude-3-5-haiku-20241022",
        "claude-3-5-sonnet-20241022",
        # "gemini-1.5-flash",
        # "gemini-1.5-pro",
    ]

    for model in models:
        evaluate(model)


def print_results():
    import pandas as pd

    folder = env.RESULTS_DIR
    files = folder.glob("*.pickle")
    files = list(files)
    print(f"Found {len(files)} results")

    results: list[Result] = []
    for file in files:
        with open(file, "rb") as f:
            result = pickle.load(f)
            results.append(result)

    results.sort(key=lambda r: r.timestamp)

    # for result in results:
    #     print(f"{result.llm} vs Stockfish {result.stockfish_elo}")
    #     print(f"Winner: {result.outcome.winner_name} in {len(result.moves)} moves")

    df = pd.DataFrame(results)
    df["n_moves"] = df.moves.apply(lambda m: math.floor(len(m) / 2))
    df["winner"] = df.outcome.apply(lambda o: o["winner_name"])
    df["reason"] = df.outcome.apply(lambda o: o["termination"])

    print(
        df[
            [
                "winner",
                "reason",
                "white",
                "black",
                "n_moves",
                "time_taken_s",
                "timestamp",
            ]
        ]
    )


if __name__ == "__main__":

    import fire

    fire.Fire({"models": models, "print_results": print_results, "evaluate": evaluate})
