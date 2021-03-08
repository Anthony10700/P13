"""
url urlpatterns of purbeurre app
"""
from django.urls import path
from . import views


urlpatterns = [
     path('connect', views.connect,
          name="connect"),
     path('sign_in.html', views.sign_in,
          name="sign_in"),
     path('account.html', views.account,
          name="account"),
     path('deconnection', views.logout_view,
          name="deconnection"),
]