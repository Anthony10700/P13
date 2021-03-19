from django.shortcuts import render, HttpResponse, redirect
import json
from django.contrib import messages
from chess_app.services.chess_app_services import lc0_play_next_move, \
    stockfish_play_next_move, komodo_play_next_move, make_new_game,\
    save_last_move, save_move_engine, get_all_games_of_specify_user, get_page, \
    get_the_game_services, analyse_game
import threading
from braces.views import LoginRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model
# Create your views here.


# class UserListView(LoginRequiredMixin, generic.ListView):
#     model = get_user_model()
#     # These next two lines tell the view to index lookups by username
#     slug_field = 'username'
#     slug_url_kwarg = 'username'
#     template_name = 'chess_app/users.html'
#     login_url = 'admin/'


def get_list_of_evalutation(request):
    """This viewe send the list of elvalution of the game,
     requiered game id in request

    Args:
        request ([type]): [description]
    """
    if "time" in request.GET:
        time = int(request.GET["time"])
    else:
        time = 0
    if time < 10:
        context = {}
        game = get_the_game_services(request)
        if game is not None:
            list_of_process = []
            list_of_process.append(
                threading.Thread(
                    target=analyse_game,
                    args=(
                        "lc0",
                        game.pgn,                        
                        time,
                        context)))

            list_of_process.append(
                threading.Thread(
                    target=analyse_game,
                    args=(
                        "stockfish",
                        game.pgn,                        
                        time,
                        context)))

            list_of_process.append(
                threading.Thread(
                    target=analyse_game,
                    args=(
                        "komodo12",
                        game.pgn,                        
                        time,
                        context)))

            for proc in list_of_process:
                proc.start()

            for proc in list_of_process:
                proc.join()

            game.analyse_list_move_lc0 = context["lc0"]
            game.analyse_list_move_komodo = context["komodo12"]
            game.analyse_list_move_stockfish = context["stockfish"]
            game.save()
            return HttpResponse(json.dumps(context))
        elif game is None:
            if "pgn" in request.GET:
                pgn = request.GET["pgn"]
                list_of_process = []
                list_of_process.append(
                    threading.Thread(
                        target=analyse_game,
                        args=(
                            "lc0",
                            pgn,                           
                            time,
                            context)))

                list_of_process.append(
                    threading.Thread(
                        target=analyse_game,
                        args=(
                            "stockfish",
                            pgn,                           
                            time,
                            context)))

                list_of_process.append(
                    threading.Thread(
                        target=analyse_game,
                        args=(
                            "komodo12",
                            pgn,                            
                            time,
                            context)))

                for proc in list_of_process:
                    proc.start()

                for proc in list_of_process:
                    proc.join()

                return HttpResponse(json.dumps(context))
    else:
        context = {"error":
                   "time per movement too large, less than ten recommend"}

        return HttpResponse(json.dumps(context))


def index(request):
    """This view concern the index of the main page

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {'title': "chess at",
               "user_is_connect": False}
    if request.user.is_authenticated:
        context["user_is_connect"] = True
    return render(request, 'chess_app/index.html', context=context)


def show_the_game(request):
    """This views show the game of chess ,
    There must be in the request , the id of the game.

    Args:
        request ([type]): [description]
    """
    game = get_the_game_services(request)
    if game is not None:
        if request.user.is_authenticated:
            context = {
                'title': "Chess game viewer",
                "user_is_connect": True,
                "games": game}
            return render(
                request,
                'chess_app/show_the_game.html',
                context=context)
        else:
            context = {
                'title': "Chess game viewer",
                "user_is_connect": False,
                "games": game}
            return render(
                request,
                'chess_app/show_the_game.html',
                context=context)
    else:
        if request.user.is_authenticated:
            context = {
                'title': "Chess game viewer",
                "user_is_connect": True}
            return render(
                request,
                'chess_app/show_the_game.html',
                context=context)
        else:
            context = {
                'title': "Chess game viewer",
                "user_is_connect": False}
            return render(
                request,
                'chess_app/show_the_game.html',
                context=context)
        return redirect("index")
        

def get_fen(request):
    """This views get best move uci 

    Args:
        request ([type]): reqruiement {"module" = "lc0"} for example

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        if "fen" in request.GET:
            fen = request.GET["fen"]
        else:
            context = {"new_fen": ""}
            return HttpResponse(json.dumps(context))
        if request.GET["module"] == "lc0":
            save_last_move(request)
            next_move = lc0_play_next_move(fen)
            save_move_engine(request.GET["game_id_current"],
                             next_move, fen)
        elif request.GET["module"] == "stockfish":
            save_last_move(request)
            next_move = stockfish_play_next_move(fen)
            save_move_engine(request.GET["game_id_current"],
                             next_move, fen)
        elif request.GET["module"] == "komodo":
            save_last_move(request)
            next_move = komodo_play_next_move(fen)
            save_move_engine(request.GET["game_id_current"],
                             next_move, fen)
        context = {"new_fen": next_move}
        return HttpResponse(json.dumps(context))
    else:
        context = {
            'title': "chess at",
            "user_is_connect": False}
        return render(request, 'chess_app/index.html', context=context)


def history_game(request):
    """This views represent the history of game of user

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """

    context = {'title': "History of your games",
               "user_is_connect": False}
    if request.user.is_authenticated:
        all_games = get_all_games_of_specify_user(request)
        context["user_is_connect"] = True
        if len(all_games) > 6:
            if "page" in request.GET:
                context["games"], context["paginate"] = get_page(
                    request.GET["page"], all_games, 6)
            else:
                context["games"], context["paginate"] = get_page(
                    1, all_games, 6)
            context["paginate"] = True
        else:
            context["paginate"] = False
            context["games"] = all_games
        return render(request, 'chess_app/history_game.html', context=context)
    else:
        messages.error(
            request, "Create an account")
        context = {
            'title': "chess at",
            "user_is_connect": False}
        return render(request, 'chess_app/index.html', context=context)


def play_vs_lc0(request):
    """Views for module play vs lc0

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        context = {
            "title": "Play vs lc0",
            "play_vs_engine": "True",
            "user_is_connect": True}
        return render(request, 'chess_app/play_vs_lc0.html', context=context)
    else:
        messages.error(
            request, "Create an account for playing against the computer")
        context = {
            'title': "chess at",
            "user_is_connect": False}
        return render(request, 'chess_app/index.html', context=context)


def play_vs_stockfish(request):
    """Views for module play vs stockfish

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        context = {
            "title": "Play vs stockfish",
            "play_vs_engine": "True",
            "user_is_connect": True}
        return render(
            request,
            'chess_app/play_vs_stockfish.html',
            context=context)
    else:
        messages.error(
            request, "Create an account for playing against the computer")
        context = {
            'title': "chess at",
            "user_is_connect": False}
        return render(request, 'chess_app/index.html', context=context)


def play_vs_komodo(request):
    """Views for module play vs komodo

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        context = {
            "title": "Play vs komodo",
            "play_vs_engine": "True",
            "user_is_connect": True}
        return render(
            request,
            'chess_app/play_vs_komodo.html',
            context=context)
    else:
        messages.error(
            request, "Create an account for playing against the computer")
        context = {
            'title': "chess at",
            "user_is_connect": False}
        return render(request, 'chess_app/index.html', context=context)

    # TODO ajouter en live l'analyse direct sans graph
    # TODO ajouter pendule
    # TODO add play human match, add bdd , add model
    # TODO add bot lc0 match lvl
    # TODO add analyse , add graph.


def new_game(request):
    """This methodes make new game with engine on click en btn new_game

    Args:
        request ([type]): [description]
    """
    if request.user.is_authenticated:
        id_of_game = make_new_game(
            request.GET["module"],
            request.user, request.GET["user_color"])
        context = {"message": "game_created", "game_id": id_of_game}
        return HttpResponse(json.dumps(context))
    else:
        messages.error(
            request, "Create an account for playing against the computer")
        context = {
            'title': "chess at",
            "user_is_connect": False}
        return render(request, 'chess_app/index.html', context=context)
