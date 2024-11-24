from game.system_prompt import SYSTEM_PROMPT
from game.types import LLMMessage, Player
from game.util import display_board_emoji, pgn_from_board


import chess
from litellm import completion


class LLMPlayer(Player):
    def __init__(self, name: LLMModel, n_attempts: int = 3, debug=False):
        self.name = name
        self.n_attempts = n_attempts
        self.debug = debug
        self.total_failed_attempts = 0
        self.failed_attempts_per_move: list[int] = []

    def get_move(self, board: chess.Board) -> chess.Move:
        messages = self.get_prompt_messages(board)

        response: str = ""

        for i in range(self.n_attempts):
            try:
                response = self.completion(messages)
                move = board.parse_san(response)
                self.failed_attempts_per_move.append(i)
                self.total_failed_attempts += i
                return move
            except chess.IllegalMoveError:
                pass
            except chess.InvalidMoveError:
                pass

        n_moves = len(board.move_stack)

        if self.debug:
            display_board_emoji(board)
            print("Attempted: ", response)

            breakpoint()

        raise ValueError(f"Failed to get a valid move after {n_moves} moves")

    def completion(self, messages: list[LLMMessage]) -> str:
        response = completion(
            model=self.name,
            messages=messages,
        )
        message = response.choices[0].message.content  # type: ignore

        if not isinstance(message, str):
            raise ValueError("LLM response is not a string")

        return message

    def get_prompt_messages(self, board: chess.Board) -> list[LLMMessage]:
        messages = [self.get_system_prompt(), self.get_user_prompt(board)]

        return messages

    def get_system_prompt(self) -> LLMMessage:

        return {
            "content": SYSTEM_PROMPT,
            "role": "system",
        }

    def get_user_prompt(self, board: chess.Board) -> LLMMessage:
        moves = pgn_from_board(board)
        return {"content": moves, "role": "user"}
