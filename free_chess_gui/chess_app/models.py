from django.db import models
from django.conf import settings
# Create your models here.


class Game_chess(models.Model):
    """This models  represents a game chess model with information

    Args:
        models ([type]): [description]
    """
    class Meta:
        ordering = ['-id']
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return self.id

    player_white = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     related_name="player_white",
                                     name="player_white",
                                     on_delete=models.CASCADE)
    player_black = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     related_name="player_black",
                                     name="player_black",
                                     on_delete=models.CASCADE)
    pgn = models.CharField(
        max_length=8000, unique=False, null=True)
    last_fen = models.CharField(
        max_length=80, unique=False, null=False)
    last_move = models.CharField(
        max_length=5, unique=False, null=True)
    analyse_list_move_lc0 = models.CharField(
        max_length=8000, unique=False, null=True)
    analyse_list_move_stockfish = models.CharField(
        max_length=8000, unique=False, null=True)
    analyse_list_move_komodo = models.CharField(
        max_length=8000, unique=False, null=True)
    chat_of_game = models.CharField(
        max_length=100000, unique=False, null=True)
