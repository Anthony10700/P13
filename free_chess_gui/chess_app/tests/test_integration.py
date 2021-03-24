"""class of test Services ChessApp."""
from django.test import RequestFactory, TransactionTestCase, Client
from django.contrib.auth import get_user_model
from chess_app.services.chess_app_services import get_page, \
    get_all_games_of_specify_user, save_move_engine, add_last_move_to_pgn, \
    save_last_move, make_new_game, lc0_play_next_move, \
    stockfish_play_next_move, komodo_play_next_move, analyse_game
from chess_app.views import get_fen, get_list_of_evalutation, index, \
    show_the_game, history_game, play_vs_lc0, play_vs_stockfish, \
    play_vs_komodo, new_game
from chess_app.models import Game_chess
import json
from django.contrib.auth.models import AnonymousUser


from django.contrib.messages.storage.fallback import FallbackStorage


class TestChessAppIntegration(TransactionTestCase):
    """class of test Services Auth integration.

    Args:
        TransactionTestCase ([type]): TransactionTestCase and not
        TestCase because Every test needs "setUp method"
    """
    reset_sequences = True

    def setUp(self):
        """[summary]"""
        # Every test needs a client.
        self.factory = RequestFactory()
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='frost', email='frost@test.fr', password='top_secret')
        self.user2 = get_user_model().objects.create_user(
            username='frost10', email='frost10@test.fr', password='top_secret')
        Game_chess.objects.create(
            pgn='[Event "Chess game AT"][Site "?"][Date "????.??.??"]'
            '[Round "?"]''[White "?"][Black "?"][Result "*"]1. Nf3 d5 2.'
            ' c4 d4 3. b4 c5 4. e3 Nf6 *',
            last_fen='rnbqkb1r/pp2pppp/5n2/2p5/1PPp4/4PN2/P2P1PPP/RNBQKB1R '
            'w KQkq - 1 5',
            last_move='g8f6',
            player_black=self.user,
            player_white=self.user2)
        Game_chess.objects.create(
            pgn='[Event "Chess game AT"][Site "?"][Date "????.??.??"]'
            '[Round "?"]''[White "?"][Black "?"][Result "*"]1. Nf3 d5 2.'
            ' c4 d4 3. b4 c5 4. e3 *',
            last_fen='rnbqkbnr/pp2pppp/8/2p5/1PPp4/4PN2/P2P1PPP/RNBQKB1R'
            ' b KQkq - 0 4',
            last_move='e2e3',
            player_black=self.user,
            player_white=self.user2)

    def test_get_page(self):
        """This method test get_page."""
        product_show = Game_chess.objects.filter(
            id='1')
        recherche, paginate = get_page(1, product_show, 6)

        self.assertEqual(recherche[0].last_move, 'g8f6')
        self.assertEqual(paginate, False)

    def test_get_all_games_of_specify_user(self):
        """This methode test the get_all_games_of_specify_user services."""
        queryset_games = Game_chess.objects.filter(
            player_white=self.user2) | Game_chess.objects.filter(
            player_black=self.user2)
        queryset_games = queryset_games.filter(last_move__isnull=False)

        self.assertEqual(
            get_all_games_of_specify_user(self.user2)[0].last_move,
            queryset_games[0].last_move)

    def test_add_last_move_to_pgn(self):
        """This methode test the add_last_move_to_pgn services."""
        last_move = 'g8f6'
        pgn = '1. Nf3 d5 2. c4 d4 3. b4 c5 4. e3 *'
        last_fen = 'rnbqkbnr/pp2pppp/8/2p5/1PPp4/4PN2/P2P1PPP/'
        'RNBQKB1R b KQkq - 0 4'
        verify_last_fen = 'rnbqkb1r/pp2pppp/5n2/2p5/1PPp4/4PN2/P2P1PPP/'
        'RNBQKB1R w KQkq - 1 5'
        verify_pgn, return_last_fen = add_last_move_to_pgn(
            last_move,
            pgn,
            from_uci=False,
            last_fen_player=last_fen)
        self.assertEqual(return_last_fen, verify_last_fen)

    def test_save_move_engine(self):
        """This methode test save_move_engine services."""
        last_move = 'g8f6'
        last_fen = 'rnbqkbnr/pp2pppp/8/2p5/1PPp4/4PN2/P2P1PPP/'
        'RNBQKB1R b KQkq - 0 4'
        save_move_engine(2, last_move, last_fen)
        queryset_games = Game_chess.objects.get(id=2)
        verify_last_fen = 'rnbqkb1r/pp2pppp/5n2/2p5/1PPp4/4PN2/P2P1PPP/'
        'RNBQKB1R w KQkq - 1 5'
        self.assertEqual(queryset_games.last_fen, verify_last_fen)

    def test_save_last_move(self):
        """This methode test save_last_move services."""
        queryset_games = Game_chess.objects.get(id=2)
        last_fen = 'rnbqkbnr/pp2pppp/8/2p5/1PPp4/4PN2/P2P1PPP/'
        'RNBQKB1R b KQkq - 0 4'
        verify_last_fen = 'rnbqkb1r/pp2pppp/5n2/2p5/1PPp4/4PN2/P2P1PPP/'
        'RNBQKB1R w KQkq - 1 5'
        self.assertEqual(queryset_games.last_fen, last_fen)
        user = get_user_model()
        info = {
            'game_id_current': 2,
            'last_move': 'g8f6',
            'fen': last_fen}
        request = self.factory.get('/chess_app/get_fen', data=info)

        request.user = user.objects.get(username='frost')
        save_last_move(request)
        queryset_games = Game_chess.objects.get(id=2)
        self.assertEqual(queryset_games.last_fen, verify_last_fen)

    def test_make_new_game(self):
        """This methode test make_new_game services."""
        user = get_user_model()
        user_get = user.objects.get(username='frost')
        self.assertEqual(make_new_game('frost', user_get, 'white'), 3)

    def test_lc0_play_next_move(self):
        """This methode test lc0_play_next_move services."""
        fen = 'rnbqkbnr/pppp1ppp/8/8/6P1/P4N1P/1PPPPp2/'
        'RNBQKB1R w KQkq - 0 5'
        move = lc0_play_next_move(fen)
        self.assertEqual(move, 'e1f2')

    def test_stockfish_play_next_move(self):
        """This methode test stockfish_play_next_move services."""
        fen = 'rnbqkbnr/pppp1ppp/8/8/6P1/P4N1P/1PPPPp2/'
        'RNBQKB1R w KQkq - 0 5'
        move = stockfish_play_next_move(fen)
        self.assertEqual(move, 'e1f2')

    def test_komodo_play_next_move(self):
        """This methode test komodo_play_next_move services."""
        fen = 'rnbqkbnr/pppp1ppp/8/8/6P1/P4N1P/1PPPPp2/'
        'RNBQKB1R w KQkq - 0 5'
        move = komodo_play_next_move(fen)
        self.assertEqual(move, 'e1f2')

    def test_analyse_game_stockfish(self):
        """This methode test analyse_game services."""
        context = {}
        analyse_game('stockfish', '1. e4 e5', 1, context)
        self.assertEqual(len(context['stockfish']), len([0.23, 0.28]))

    def test_analyse_game_komodo(self):
        """This methode test analyse_game services."""
        context = {}
        analyse_game('komodo12', '1. e4 e5', 1, context)
        self.assertEqual(len(context['komodo12']), len([0.23, 0.28]))

    def test_analyse_game_lco(self):
        """This methode test analyse_game services."""
        context = {}
        analyse_game('lc0', '1. e4 e5', 1, context)
        self.assertEqual(len(context['lc0']), len([0.23, 0.28]))


class TestUrlAuth(TransactionTestCase):
    """Class test of url of app auth (test views)

    Args:
        TestCase ([type]): [description]
    """

    def setUp(self):
        """This method similar at __init__ for each instance."""
        # Every test needs a client.
        self.factory = RequestFactory()
        self.client = Client()
        user_intance = get_user_model()
        self.user = user_intance.objects.create_user(
            username='frost', email='frost@test.fr', password='top_secret')
        self.user2 = user_intance.objects.create_user(
            username='frost10', email='frost10@test.fr', password='top_secret')
        Game_chess.objects.create(
            pgn='[Event "Chess game AT"][Site "?"][Date "????.??.??"]'
            '[Round "?"][White "?"][Black "?"][Result "*"]1. Nf3 d5 '
            '2. c4 d4 3. b4 c5 4. e3 Nf6 *',
            last_fen='rnbqkb1r/pp2pppp/5n2/2p5/1PPp4/4PN2/P2P1PPP/'
            'RNBQKB1R w KQkq - 1 5',
            last_move='g8f6',
            player_black=self.user,
            player_white=self.user2)
        Game_chess.objects.create(
            pgn='[Event "Chess game AT"][Site "?"][Date "????.??.??"]'
            '[Round "?"][White "?"][Black "?"][Result "*"]1. Nf3 d5 '
            '2. c4 d4 3. b4 c5 4. e3 *',
            last_fen='rnbqkbnr/pp2pppp/8/2p5/1PPp4/4PN2/P2P1PPP/'
            'RNBQKB1R b KQkq - 0 4',
            last_move='e2e3',
            player_black=self.user,
            player_white=self.user2)
        Game_chess.objects.create(
            pgn='[Event "Chess game AT"][Site "?"][Date "????.??.??"]'
            '[Round "?"][White "?"][Black "?"][Result "*"]1. Nf3 d5 '
            '2. c4 d4 3. b4 c5 4. e3 *',
            last_fen='rnbqkbnr/pp2pppp/8/2p5/1PPp4/4PN2/P2P1PPP/'
            'RNBQKB1R b KQkq - 0 4',
            last_move='e2e3',
            player_black=self.user,
            player_white=self.user2)

        for game in Game_chess.objects.all():
            print('game : = ', game.id)
            self.last_game = game.id

    def test_get_list_of_evalutation(self):
        """This method test the get_list_of_evalutation url."""
        pgn = '[Event "Chess game AT"][Site "?"][Date "????.??.??"]'
        '[Round "?"][White "?"][Black "?"][Result "*"]1. Nf3 d5 '
        '2. c4 d4 3. b4 c5 4. e3 *'
        info = {'id': self.last_game, 'pgn': pgn}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/get_list_of_evalutation/', data=info)

        request.user = user.objects.get(username='frost10')
        response = get_list_of_evalutation(request)
        list_eval = json.loads(response.content)
        self.assertEqual(len(list_eval), 3)

        info = {'id': self.last_game, 'pgn': pgn, 'time': 100}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/get_list_of_evalutation/', data=info)

        request.user = user.objects.get(username='frost10')
        response = get_list_of_evalutation(request)
        list_eval = json.loads(response.content)
        self.assertEqual(
            list_eval['error'],
            'time per movement too large, less than ten recommend')

        info = {'id': 234556, 'pgn': pgn}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/get_list_of_evalutation/', data=info)

        request.user = user.objects.get(username='frost10')
        response = get_list_of_evalutation(request)
        list_eval = json.loads(response.content)
        self.assertEqual(len(list_eval), 3)

        info = {'id': 1234556}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/get_list_of_evalutation/', data=info)

        request.user = user.objects.get(username='frost10')
        response = get_list_of_evalutation(request)
        list_eval = json.loads(response.content)
        self.assertEqual(len(list_eval), 0)

    def test_index(self):
        """This method test the index url."""
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/index.html')

        request.user = user.objects.get(username='frost10')
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_show_the_game(self):
        """This method test the show_the_game url."""
        info = {'id': self.last_game}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/show_the_game.html', data=info)

        request.user = user.objects.get(username='frost10')
        response = show_the_game(request)
        self.assertEqual(response.status_code, 200)

        info = {'id': self.last_game}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/show_the_game.html', data=info)

        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = show_the_game(request)
        self.assertEqual(response.status_code, 200)

        info = {'id': 2345}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/show_the_game.html', data=info)

        request.user = user.objects.get(username='frost10')
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = show_the_game(request)
        self.assertEqual(response.status_code, 200)

        info = {'id': 2345}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/show_the_game.html', data=info)

        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = show_the_game(request)
        self.assertEqual(response.status_code, 200)

    def test_get_fen(self):
        """This method test the get_fen url."""
        fen = 'rnbqkbnr/pppp1ppp/8/8/6P1/P4N1P/1PPPPp2/'
        'RNBQKB1R w KQkq - 0 5'
        info = {
            'fen': fen,
            'module': 'stockfish',
            'game_id_current': self.last_game}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/get_fen', data=info)

        request.user = user.objects.get(username='frost10')
        response = get_fen(request)
        self.assertEqual(response.status_code, 200)

        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = get_fen(request)
        self.assertEqual(response.status_code, 200)

        info = {
            'module': 'stockfish',
            'game_id_current': self.last_game}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/get_fen', data=info)

        request.user = user.objects.get(username='frost10')
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = get_fen(request)
        self.assertEqual(response.status_code, 200)

        # lc0
        info = {
            'fen': fen,
            'module': 'lc0',
            'game_id_current': self.last_game}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/get_fen', data=info)

        request.user = user.objects.get(username='frost10')
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = get_fen(request)
        self.assertEqual(response.status_code, 200)

        # komodo

        info = {
            'fen': fen,
            'module': 'komodo',
            'game_id_current': self.last_game}
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/get_fen', data=info)

        request.user = user.objects.get(username='frost10')
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = get_fen(request)
        self.assertEqual(response.status_code, 200)

    def test_history_game(self):
        """This method test the history_game url."""
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/history_game.html')

        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = history_game(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(
            '/chess_app/history_game.html')
        request.user = user.objects.get(username='frost10')
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = history_game(request)
        self.assertEqual(response.status_code, 200)

    def test_play_vs_lc0(self):
        """This method test the play_vs_lc0 url."""
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/play_vs_lc0.html')

        request.user = user.objects.get(username='frost10')
        response = play_vs_lc0(request)
        self.assertEqual(response.status_code, 200)

        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        request.user = AnonymousUser()
        response = play_vs_lc0(request)
        self.assertEqual(response.status_code, 200)

    def test_play_vs_stockfish(self):
        """This method test the play_vs_stockfish url."""
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/play_vs_stockfish.html')

        request.user = user.objects.get(username='frost10')
        response = play_vs_stockfish(request)
        self.assertEqual(response.status_code, 200)

        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = play_vs_stockfish(request)
        self.assertEqual(response.status_code, 200)

    def test_play_vs_komodo(self):
        """This method test the play_vs_komodo url."""
        user = get_user_model()
        request = self.factory.get(
            '/chess_app/play_vs_komodo.html')

        request.user = user.objects.get(username='frost10')
        response = play_vs_komodo(request)
        self.assertEqual(response.status_code, 200)

        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = play_vs_komodo(request)
        self.assertEqual(response.status_code, 200)

    def test_new_game(self):
        """This method test the new_game url."""
        info = {
            'module': 'frost',
            'user_color': 'white',
        }

        user = get_user_model()
        request = self.factory.get(
            '/chess_app/new_game', data=info)

        request.user = user.objects.get(username='frost10')
        response = new_game(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(
            '/chess_app/new_game', data=info)
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = new_game(request)
        self.assertEqual(response.status_code, 200)
