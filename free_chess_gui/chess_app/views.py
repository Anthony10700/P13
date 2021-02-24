from django.shortcuts import render, HttpResponse
import json
from chess_app.services.chess_app_services import lc0_play_next_move, \
    stockfish_play_next_move, komodo_play_next_move
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
    if request.GET["module"] == "lc0":
        next_move = lc0_play_next_move(fen)
    elif request.GET["module"] == "stockfish":
        next_move = stockfish_play_next_move(fen)
    elif request.GET["module"] == "komodo":
        next_move = komodo_play_next_move(fen)
    
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
    context = {"title": "Play vs stockfish"}
    return render(request, 'chess_app/play_vs_stockfish.html', context=context)


def play_vs_komodo(request):
    """Views for module play vs komodo

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {"title": "Play vs komodo"}
    return render(request, 'chess_app/play_vs_komodo.html', context=context)

    # TODO status div, faire en sorte quelle dessendre avec bar
    # TODO add premove
    # TODO add takeback
    # TODO add check red pieces
    # TODO ajouter en live l'analyse direct sans graph
    # TODO add play human match, add bdd , add model
    # TODO add bot lc0 match lvl
    # TODO add analyse , add graph.
