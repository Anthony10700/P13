# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(
        regex=r'^dialogs/(?P<username>[\w.@+-]+)$',
        view=views.DialogListView.as_view(),
        name='dialogs_detail'
    ),
    url(
        regex=r'^dialogs/$',
        view=views.DialogListView.as_view(),
        name='dialogs'
    ),
    path(
        'connect_required.html',
        view=views.connect_required,
        name='connect_required'
    ),
]
