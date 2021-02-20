import chess
import chess.engine
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
engine_lc0 = chess.engine.SimpleEngine.popen_uci(str(BASE_DIR) + "/lc0/lc0.exe")
engine_stockfish = chess.engine.SimpleEngine.popen_uci(str(BASE_DIR) + "/stockfish/stockfish.exe")


def uci_play_next_move(fen):
    """This method get fen and return next move

    Args:
        fen ([type]): [description]
    """
    board = chess.Board(fen)
    print("board = ", board)
    # result = engine.play(board, chess.engine.Limit(time=5))
    info = engine_stockfish.analyse(board, chess.engine.Limit(time=1))
    print(info["score"])
    print(info["pv"])
    return str(info["pv"][0])
    # engine.quit()