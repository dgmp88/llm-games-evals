from abc import ABC
from dataclasses import dataclass
from typing import Literal

import chess
from litellm import TypedDict

LLMModel = Literal[
    # https://docs.litellm.ai/docs/providers
    # OpenAI
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-05-13",
    "gpt-4o-mini-2024-07-18",
    "o1-mini",
    "o1-preview",
    # Anthropic
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
]


class LLMMessage(TypedDict):
    content: str
    role: Literal["user", "system", "assistant"]


class Player(ABC):
    name: str

    def get_move(self, board: chess.Board) -> chess.Move:
        raise NotImplementedError()


class LostByInvalidMoves(ValueError):
    """
    Too many invalid moves were made, we can't keep playing
    """

    pass


@dataclass
class Outcome:
    # chess.Termination doesn't include invalid_moves, so make our own
    termination: Literal["invalid_moves", "checkmate", "stalemate", "too_many_moves"]
    winner_name: str | None

    def __str__(self):
        return (
            f"Outcome(termination={self.termination}, winner_name={self.winner_name})"
        )
