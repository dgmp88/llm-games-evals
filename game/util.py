import chess
from chess.pgn import Game as PGNGame


PIECE_TO_EMOJI = {
    "r": "♜",
    "n": "♞",
    "b": "♝",
    "q": "♛",
    "k": "♚",
    "p": "♟",
    "R": "♖",
    "N": "♘",
    "B": "♗",
    "Q": "♕",
    "K": "♔",
    "P": "♙",
}


def get_board_emoji(board: chess.Board):
    board_str = str(board)
    for piece in PIECE_TO_EMOJI:
        board_str = board_str.replace(piece, PIECE_TO_EMOJI[piece])

    # Add in numbers and letters for the board
    lines = board_str.split("\n")
    lines = [f"{8-i}   {lines[i]}   {8-i}" for i in range(8)]

    lines = (
        ["", "    a b c d e f g h    ", ""] + lines + ["", "    a b c d e f g h    "]
    )

    board_str = "\n".join(lines)

    return board_str


def pgn_from_board(board: chess.Board) -> str:
    pgn_board = PGNGame.from_board(board)

    # Strip the headers
    pgn = str(pgn_board).split("\n")[-1]

    n_moves = len(board.move_stack)

    if n_moves % 2 == 0:
        # Put a number and dot before the * to help the LLM
        index = n_moves // 2 + 1
        pgn = pgn.replace("*", f"{index}. *")

    return pgn
