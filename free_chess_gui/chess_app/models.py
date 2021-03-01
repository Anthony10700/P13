from django.db import models
from django.conf import settings
# Create your models here.


class game(models.Model):
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
                                     name="player_white")
    player_black = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     related_name="player_black",
                                     name="player_black")
    pgn = models.CharField(
        max_length=8000, unique=False, null=False)
    last_fen = models.CharField(
        max_length=80, unique=False, null=False)
    analyse_list_move = models.CharField(
        max_length=8000, unique=False, null=False)
