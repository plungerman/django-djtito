# -*- coding: utf-8 -*-

"""URLs for newsletter manager."""

from django.urls import path
from django.views.generic import RedirectView
from djtito.newsletter import views


urlpatterns = [
    path('archives/<int:year>/', views.archives, name='newsletter_archives'),
    path('archives/', views.archives, name='newsletter_archives_default'),
    path('manager/', views.manager, name='newsletter_manager'),
    # clear livewhale blurb cache via ajax post
    path('cache/<str:ctype>/clear/', views.clear_cache, name='clear_cache'),
    path('', RedirectView.as_view(url='/bridge/')),
]
