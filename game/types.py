from abc import ABC
from typing import Literal

import chess
from litellm import TypedDict

LLMModel = Literal[
    # OpenAI
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-05-13",
    "gpt-4o-mini-2024-07-18",
    "o1-mini",
    "o1-preview",
]


class LLMMessage(TypedDict):
    content: str
    role: Literal["user", "system", "assistant"]


class Player(ABC):
    name: str

    def get_move(self, board: chess.Board) -> chess.Move:
        raise NotImplementedError()
