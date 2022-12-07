# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render


def print(request):
    """."""
    return render(request, 'catalog/print.html', {})
