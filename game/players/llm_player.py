from game.system_prompt import SYSTEM_PROMPT
from game.types import LLMMessage, LostByInvalidMoves, Player, LLMModel
from game.util import get_board_emoji, pgn_from_board
from litellm import completion


import chess


class LLMPlayer(Player):
    def __init__(
        self,
        name: LLMModel,
        n_attempts: int = 1,
        debug: bool = False,
        board_provided: bool = False,
    ):
        self.name = name
        self.n_attempts = n_attempts
        self.debug = debug
        self.total_failed_attempts = 0
        self.failed_attempts_per_move: list[int] = []
        self.board_provided = board_provided

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
            except (
                chess.IllegalMoveError,
                chess.InvalidMoveError,
                chess.AmbiguousMoveError,
            ):
                pass

        n_moves = len(board.move_stack)

        if self.debug:
            emj = get_board_emoji(board)
            print(emj)
            print(f"Attempted: '{response}'")

            breakpoint()

        raise LostByInvalidMoves(f"Failed to get a valid move after {n_moves} moves")

    def completion(self, messages: list[LLMMessage]) -> str:
        response = completion(model=self.name, messages=messages, max_tokens=10)
        message = response.choices[0].message.content  # type: ignore

        if not isinstance(message, str):
            raise ValueError("LLM response is not a string")

        message = message.strip()
        message = message.split(" ")[0]
        return message

    def get_prompt_messages(self, board: chess.Board) -> list[LLMMessage]:
        messages = [self.get_system_prompt(board), self.get_user_prompt(board)]
        # messages = [self.get_system_prompt(board)]
        return messages

    def get_system_prompt(self, board: chess.Board) -> LLMMessage:

        board_str = ""
        if self.board_provided:
            emoji_board = get_board_emoji(board)
            board_str = "This is the current board state:\n\n" + emoji_board + "\n\n"

        system_prompt = SYSTEM_PROMPT.format(board=board_str)

        # Only works with openai models
        # moves = pgn_from_board(board)
        # system_prompt += "\n" + moves[:-1]
        return {
            "content": system_prompt,
            "role": "system",
        }

    def get_user_prompt(self, board: chess.Board) -> LLMMessage:
        moves = pgn_from_board(board)

        return {"content": moves, "role": "user"}


if __name__ == "__main__":
    from litellm.utils import supports_prompt_caching

    supports_pc: bool = supports_prompt_caching(model="gpt-4o-2024-08-06")

    print(supports_pc)
