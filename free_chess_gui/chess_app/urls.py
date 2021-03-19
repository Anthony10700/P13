"""
url urlpatterns of purbeurre app
"""
from django.urls import path
from . import views


urlpatterns = [
    path('index.html', views.index,
         name="index"),
    path('get_fen', views.get_fen,
         name="get_fen"),  
    path('play_vs_lc0.html', views.play_vs_lc0,
         name="play_vs_lc0"),  
    path('play_vs_stockfish.html', views.play_vs_stockfish,
         name="play_vs_stockfish"),  
    path('play_vs_komodo.html', views.play_vs_komodo,
         name="play_vs_komodo"),
    path('history_game.html', views.history_game,
         name="history_game"),
    path('new_game', views.new_game,
         name="new_game"),
    path('show_the_game.html/', views.show_the_game,
         name="show_the_game"),
    path('get_list_of_evalutation/', views.get_list_of_evalutation,
         name="get_list_of_evalutation"),
]