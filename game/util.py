import chess


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


def display_board_emoji(board: chess.Board):
    board_str = str(board)
    for piece in PIECE_TO_EMOJI:
        board_str = board_str.replace(piece, PIECE_TO_EMOJI[piece])
    print(board_str)
