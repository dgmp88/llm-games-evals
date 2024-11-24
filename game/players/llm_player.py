from game.system_prompt import SYSTEM_PROMPT
from game.types import LLMMessage, LostByInvalidMoves, Player, LLMModel
from game.util import get_board_emoji, pgn_from_board


import chess
from litellm import completion


class LLMPlayer(Player):
    def __init__(
        self,
        name: LLMModel,
        n_attempts: int = 3,
        debug: bool = False,
        insert_board: bool = False,
    ):
        self.name = name
        self.n_attempts = n_attempts
        self.debug = debug
        self.total_failed_attempts = 0
        self.failed_attempts_per_move: list[int] = []
        self.insert_board = insert_board

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
            emj = get_board_emoji(board)
            print(emj)
            print("Attempted: ", response)

            breakpoint()

        raise LostByInvalidMoves(f"Failed to get a valid move after {n_moves} moves")

    def completion(self, messages: list[LLMMessage]) -> str:
        response = completion(
            model=self.name,
            messages=messages,
        )
        message = response.choices[0].message.content  # type: ignore

        # print(response.usage) # currently nothing is cached as it's too few tokens

        if not isinstance(message, str):
            raise ValueError("LLM response is not a string")

        return message

    def get_prompt_messages(self, board: chess.Board) -> list[LLMMessage]:
        messages = [self.get_system_prompt(board), self.get_user_prompt(board)]
        return messages

    def get_system_prompt(self, board: chess.Board) -> LLMMessage:

        board_str = ""
        if self.insert_board:
            emoji_board = get_board_emoji(board)
            board_str = "This is the current board state:\n\n" + emoji_board + "\n\n"

        system_prompt = SYSTEM_PROMPT.format(board=board_str)

        return {
            "content": system_prompt,
            "role": "system",
        }

    def get_user_prompt(self, board: chess.Board) -> LLMMessage:
        moves = pgn_from_board(board)

        if len(moves) == 0:
            moves = "1. *"

        return {"content": moves, "role": "user"}


if __name__ == "__main__":
    from litellm.utils import supports_prompt_caching

    supports_pc: bool = supports_prompt_caching(model="gpt-4o-2024-08-06")

    print(supports_pc)
