import random
import time

import chess
import chess.engine
from stockfish import Stockfish

from env import env

depth = 10
time_limit_ms = 100


# Initialize board and stockfish
class Player:
    def __init__(self, name: str, elo: int):
        self.name = name

        self.stockfish = Stockfish(path=env.STOCKFISH_PATH)
        self.stockfish.set_depth(depth)
        self.stockfish.set_elo_rating(elo)

    def get_best_move(self, board: chess.Board) -> chess.Move:
        self.stockfish.set_position([move.uci() for move in board.move_stack])
        t0 = time.time()
        result = self.stockfish.get_best_move_time(time_limit_ms)
        print("Took", time.time() - t0, "seconds")
        move = chess.Move.from_uci(result)
        return move


board = chess.Board()

p1 = Player("weak", 2000)
p2 = Player("strong", 2000)

p1_first = random.choice([True, False])

white_player = p1 if p1_first else p2
black_player = p2 if p1_first else p1

piece_to_emoji = {
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


def display_board_emoji(board):
    board_str = str(board)
    for piece in piece_to_emoji:
        board_str = board_str.replace(piece, piece_to_emoji[piece])
    print(board_str)


board = chess.Board()

# Game loop
while not board.is_game_over():
    if board.turn == chess.WHITE:  # Human/Random plays White
        move = white_player.get_best_move(board)
    else:
        move = black_player.get_best_move(board)
    board.push(move)


print("\nGame Over!")

outcome = board.outcome()
print(f"Termination type: {outcome.termination.name}")

winning_player = white_player if outcome.winner == chess.WHITE else black_player
print(f"Winning player: {winning_player.name}")
