# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from djtito.catalog import views


urlpatterns = [
    path('print/', views.paint, name='paint'),
]
