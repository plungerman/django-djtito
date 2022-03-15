# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from djtito.bridge import views


urlpatterns = [
    path('screens/events/', views.events, name='events'),
    path('screens/news/', views.news, name='news'),
]
