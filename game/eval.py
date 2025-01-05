from dataclasses import dataclass, field
from datetime import datetime
import math
import pickle
import pandas as pd

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
    board_provided: bool = field(default=False)

    def save(self):
        now_str = self.timestamp.strftime("%Y-%m-%d_%H-%M-%S")

        llm_name = self.llm.replace("/", "-")
        filename = (
            f"result_{llm_name}_vs_stockfish_{self.stockfish_elo}_{now_str}.pickle"
        )

        file = env.RESULTS_DIR / filename

        with open(file, "wb") as f:
            pickle.dump(self, f)


def evaluate(
    model: LLMModel,
    debug: bool = False,
    board_provided: bool = False,
    completion_prompt: bool = False,
):

    print("Board provided: ", board_provided, "Completion prompt: ", completion_prompt)

    for i in range(10):
        for elo in [1500]:
            print(f"Evaluating model {model} against Stockfish {elo}")
            llm = LLMPlayer(
                model,
                debug=debug,
                board_provided=board_provided,
                completion_prompt=completion_prompt,
            )

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
                board_provided=board_provided,
            )

            result.save()


def models(board_provided: bool = False):
    models: list[LLMModel] = [
        # "gpt-4o-mini-2024-07-18",
        # "gpt-4o-2024-11-20",
        # "gpt-3.5-turbo-0125",
        # "gpt-3.5-turbo-instruct",
        # "claude-3-5-haiku-20241022",
        # "claude-3-5-sonnet-20241022",
        # "gemini/gemini-1.5-flash",
        # "gemini/gemini-1.5-pro",
        "gemini/gemini-2.0-flash-exp",
        # "ollama/llama3.1:8b",
        # "together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        # "together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        # "together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    ]

    for model in models:
        evaluate(model, board_provided=board_provided)


def get_results_df() -> pd.DataFrame:

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
    df = pd.DataFrame(results).assign(
        n_moves=lambda x: x.moves.apply(lambda m: math.floor(len(m) / 2)),
        winner=lambda x: x.outcome.apply(lambda o: o["winner_name"]),
        reason=lambda x: x.outcome.apply(lambda o: o["termination"]),
    )

    return df


def print_results():
    df = get_results_df()

    print(
        df[
            [
                "winner",
                "reason",
                "white",
                "black",
                "n_moves",
                "board_provided",
                "time_taken_s",
                "timestamp",
            ]
        ]
    )

    print(df.groupby("llm").n_moves.agg(["mean", "min", "max", "std"]))

    print(df.groupby("stockfish_elo").n_moves.agg(["mean", "median", "max"]))
    print(df.groupby("board_provided").n_moves.agg(["mean", "median", "max"]))


if __name__ == "__main__":

    import fire

    fire.Fire({"models": models, "print_results": print_results, "evaluate": evaluate})
