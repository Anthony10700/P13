import chess
import chess.engine
from pathlib import Path
from chess_app.models import Game_chess
from django.contrib.auth import get_user_model
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


def make_new_game(module_name, user, user_color):
    """This methode make new game to engine

    Args:
        module_name ([type]): [description]
        user ([type]): [description]
    """
    engine_user = get_user_model()
    engine = engine_user.objects.get(username=module_name)
    if user_color == "white":
        new_game = Game_chess.objects.create(
            player_white=user,
            player_black=engine,
            pgn="",
            last_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    else:
        new_game = Game_chess.objects.create(
            player_white=engine,
            player_black=user,
            pgn="",
            last_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    new_game.save()
    return new_game.id


def lc0_play_next_move(fen, time_per_move=1):
    """This method get fen and return next move for lc0

    Args:
        fen ([type]): [description]
    """
    engine_lc0 = chess.engine.SimpleEngine.popen_uci(str(BASE_DIR) + "/lc0/lc0.exe")
    board = chess.Board(fen)
    print("board = ", fen)
    # result = engine.play(board, chess.engine.Limit(time=5))
    info = engine_lc0.analyse(board, chess.engine.Limit(time=time_per_move))
    print(info["score"])
    print(info["pv"])
    engine_lc0.quit()
    return str(info["pv"][0])


def stockfish_play_next_move(fen, time_per_move=1):
    """This method get fen and return next move for stockfish

    Args:
        fen ([type]): [description]
    """
    engine_stockfish = chess.engine.SimpleEngine.popen_uci(str(BASE_DIR) + "/stockfish/stockfish.exe")
    board = chess.Board(fen)
    print("board = ", fen)
    # result = engine.play(board, chess.engine.Limit(time=5))
    info = engine_stockfish.analyse(
        board, chess.engine.Limit(time=time_per_move))
    print(info["score"])
    print(info["pv"])
    engine_stockfish.quit()
    return str(info["pv"][0])


def komodo_play_next_move(fen, time_per_move=1):
    """This method get fen and return next move for komodo

    Args:
        fen ([type]): [description]
    """
    komodo = chess.engine.SimpleEngine.popen_uci(str(BASE_DIR) + "/komodo12/Windows/komodo-12.1.1-64bit.exe")
    board = chess.Board(fen)
    print("board = ", fen)
    # result = engine.play(board, chess.engine.Limit(time=5))
    info = komodo.analyse(board, chess.engine.Limit(time=time_per_move))
    print(info["score"])
    print(info["pv"])
    komodo.quit()
    return str(info["pv"][0])