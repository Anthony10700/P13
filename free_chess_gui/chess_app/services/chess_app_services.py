import chess
import chess.engine
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
engine_lc0 = chess.engine.SimpleEngine.popen_uci(str(BASE_DIR) + "/lc0/lc0.exe")
engine_stockfish = chess.engine.SimpleEngine.popen_uci(str(BASE_DIR) + "/stockfish/stockfish.exe")
komodo = chess.engine.SimpleEngine.popen_uci(str(BASE_DIR) + "/komodo12/Windows/komodo-12.1.1-64bit.exe")


def lc0_play_next_move(fen):
    """This method get fen and return next move for lc0

    Args:
        fen ([type]): [description]
    """
    board = chess.Board(fen)
    print("board = ", fen)
    # result = engine.play(board, chess.engine.Limit(time=5))
    info = engine_lc0.analyse(board, chess.engine.Limit(time=1))
    print(info["score"])
    print(info["pv"])
    return str(info["pv"][0])


def stockfish_play_next_move(fen):
    """This method get fen and return next move for stockfish

    Args:
        fen ([type]): [description]
    """
    board = chess.Board(fen)
    print("board = ", fen)
    # result = engine.play(board, chess.engine.Limit(time=5))
    info = engine_stockfish.analyse(board, chess.engine.Limit(time=1))
    print(info["score"])
    print(info["pv"])
    return str(info["pv"][0])


def komodo_play_next_move(fen):
    """This method get fen and return next move for komodo

    Args:
        fen ([type]): [description]
    """
    board = chess.Board(fen)
    print("board = ", fen)
    # result = engine.play(board, chess.engine.Limit(time=5))
    info = komodo.analyse(board, chess.engine.Limit(time=1))
    print(info["score"])
    print(info["pv"])
    return str(info["pv"][0])