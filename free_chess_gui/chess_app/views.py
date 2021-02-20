from django.shortcuts import render, HttpResponse
import json
from chess_app.services.chess_app_services import uci_play_next_move
# Create your views here.


def index(request):
    """This view concern the index of the main page

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {'title': "chess at"}
    return render(request, 'chess_app/index.html', context=context)


def get_fen(request):
    fen = request.GET["fen"]
    print(fen)
    next_move = uci_play_next_move(fen)
    print(next_move)
    context = {"new_fen": next_move}
    return HttpResponse(json.dumps(context))


def play_vs_lc0(request):
    """Views for module play vs lc0

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {"title": "Play vs lc0"}
    return render(request, 'chess_app/play_vs_lc0.html', context=context)


def play_vs_stockfish(request):
    """Views for module play vs stockfish

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {"title": "Play vs lc0"}
    return render(request, 'chess_app/play_vs_lc0.html', context=context)


def play_vs_komodo(request):
    """Views for module play vs komodo

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {"title": "Play vs lc0"}
    return render(request, 'chess_app/play_vs_lc0.html', context=context)