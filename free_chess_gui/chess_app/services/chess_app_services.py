import chess
import chess.engine
import chess.pgn
from pathlib import Path
from chess_app.models import Game_chess
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import io
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


def get_page(page, all_game, nb_of_articles_per_page):
    """This method make a paginator of all products

    Args:
        page (int): page of paginator
        all_game (Product): product
        nb_of_articles_per_page (int): number of articles per page

    Returns:
        tuple: nb_of_articles_per_page product and paginate.
        paginate in context is for: True the button show in html page,
        False the button no visible
    """
    paginator = Paginator(all_game, nb_of_articles_per_page)

    try:
        recherche = paginator.page(page)
    except PageNotAnInteger:
        recherche = paginator.page(1)
    except EmptyPage:
        recherche = paginator.page(paginator.num_pages)

    if paginator.num_pages > 1:
        paginate = True
    else:
        paginate = False

    return recherche, paginate

def get_all_games_of_specify_user(request):
    """This method get all game of user

    Args:
        request ([type]): [description]
    """
    queryset_games = Game_chess.objects.filter(
        player_white=request.user.id) | Game_chess.objects.filter(
            player_black=request.user.id)
    queryset_games = queryset_games.filter(last_move__isnull=False)
    return queryset_games


def save_move_engine(game_id_current, last_move, last_fen_player):
    """This methodes save the last move of engine chess

    Args:
        last_move ([type]): [description]
    """
    game = Game_chess.objects.get(id=game_id_current)
    game.last_move = last_move
    game.pgn, game.last_fen = add_last_move_to_pgn(
        last_move, game.pgn,
        from_uci=True,
        last_fen_player=last_fen_player)
    game.save()


def add_last_move_to_pgn(last_move, pgn, from_uci=False, last_fen_player=""):
    """
    This method add last move to pgn and verify if true move

    Args:
        last_move ([type]): [description]
    """
    try:
        print(pgn)
        pgn = io.StringIO(pgn)
        pgn_chess_game = chess.pgn.read_game(pgn)
        board = chess.Board()
        new_pgn_chess_game = chess.pgn.Game()
        new_pgn_chess_game.headers["Event"] = "modif"
        nb_of_move = 0
        for (i, move) in enumerate(pgn_chess_game.mainline_moves()):
            if i == 0:
                node = new_pgn_chess_game.add_variation(
                    board.push_uci(move.uci()))
            else:
                node = node.add_variation(board.push_uci(move.uci()))
            nb_of_move += 1
        if from_uci:
            if nb_of_move == 0:
                node = new_pgn_chess_game.add_variation(
                    board.push_uci(last_move))
            else:
                node = node.add_variation(
                    board.push_uci(last_move))
        else:
            if nb_of_move == 0:
                node = new_pgn_chess_game.add_variation(
                    board.push_san(last_move))
            else:
                node = node.add_variation(
                    board.push_san(last_move))
        return new_pgn_chess_game, board.fen()
    except ValueError as err:        
        if str(err)[:11] == "illegal uci":
            print(str(err)[:11])
            # TODO rajouter ici un logger pour remonter l'info
            #  sur sentry par exemple
            return pgn_chess_game, last_fen_player
        else:
            return pgn_chess_game, last_fen_player


def save_last_move(request):
    """This methode save last move of chess game to database

    Args:
        request ([type]): [description]
    """
    if "game_id_current" in request.GET and "last_move" in request.GET \
            and "fen" in request.GET:
        game = Game_chess.objects.get(id=request.GET["game_id_current"])
        game.last_move = request.GET["last_move"]
        game.pgn, game.last_fen = add_last_move_to_pgn(
            request.GET["last_move"], game.pgn)
        game.save()
    else:
        return "game_id_current and last_move and fen not in request"


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
            pgn=chess.pgn.Game(),
            last_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    else:
        new_game = Game_chess.objects.create(
            player_white=engine,
            player_black=user,
            pgn=chess.pgn.Game(),
            last_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    new_game.save()
    return new_game.id


def lc0_play_next_move(fen, time_per_move=1):
    """This method get fen and return next move for lc0

    Args:
        fen ([type]): [description]
    """
    engine_lc0 = chess.engine.SimpleEngine.popen_uci(
        str(BASE_DIR) + "/lc0/lc0.exe")
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
    engine_stockfish = chess.engine.SimpleEngine.popen_uci(
        str(BASE_DIR) + "/stockfish/stockfish.exe")
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
    komodo = chess.engine.SimpleEngine.popen_uci(
        str(BASE_DIR) + "/komodo12/Windows/komodo-12.1.1-64bit.exe")
    board = chess.Board(fen)
    print("board = ", fen)
    # result = engine.play(board, chess.engine.Limit(time=5))
    info = komodo.analyse(board, chess.engine.Limit(time=time_per_move))
    print(info["score"])
    print(info["pv"])
    komodo.quit()
    return str(info["pv"][0])
