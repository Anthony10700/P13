"""
        class of test Services Auth
    """
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from chess_app.services.chess_app_services import get_the_game_services
from chess_app.models import Game_chess


# Create your tests here.


class TestChessAppUnitaire(TransactionTestCase):
    """class of test Services Auth Unitaire API

    Args:
        TransactionTestCase ([type]): TransactionTestCase and not
        TestCase because Every test needs "setUp method"
    """
    reset_sequences = True

    def setUp(self):
        """[summary]
        """
        user = get_user_model().objects.create_user(
            username='frost', email='frost@test.fr', password='top_secret')
        Game_chess.objects.create(
            pgn='[Event "Chess game AT"][Site "?"][Date "????.??.??"]'
            '[Round "?"][White "?"][Black "?"][Result "*"]1. Nf3 d5 '
            '2. c4 d4 3. b4 c5 4. e3 Nf6 *',
            last_fen="rnbqkb1r/pp2pppp/5n2/2p5/1PPp4/4PN2/P2P1PPP"
            "/RNBQKB1R w KQkq - 1 5",
            last_move="g8f6",
            player_black=user,
            player_white=user)

    def test_get_the_game_services(self):
        """This method test the game services
        """
        game_verif = Game_chess.objects.get(id="1")
        game_get = get_the_game_services({"id": "1"})
        self.assertEqual(game_get.id, game_verif.id)
