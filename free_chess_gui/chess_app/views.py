from django.shortcuts import render, HttpResponse, redirect
import json
from django.contrib import messages
from chess_app.services.chess_app_services import lc0_play_next_move, \
    stockfish_play_next_move, komodo_play_next_move, make_new_game
# Create your views here.


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


def get_fen(request):
    if request.user.is_authenticated:
        fen = request.GET["fen"]
        if request.GET["module"] == "lc0":
            next_move = lc0_play_next_move(fen)
        elif request.GET["module"] == "stockfish":
            next_move = stockfish_play_next_move(fen)
        elif request.GET["module"] == "komodo":
            next_move = komodo_play_next_move(fen)    
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
    return redirect("index")


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
        messages.error(request, "For play vs engine you need to make account")
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
        messages.error(request, "For play vs engine you need to make account")
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
        messages.error(request, "For play vs engine you need to make account")
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
        messages.error(request, "For play vs engine you need to make account")
        context = {
            'title': "chess at",
            "user_is_connect": False}
        return render(request, 'chess_app/index.html', context=context)