# -*- coding: utf-8 -*-

import datetime
import requests

from django.conf import settings
from django.shortcuts import render
from djtito.core.models import LivewhaleEvents as Events
from djtito.core.models import LivewhaleNews as News
from djtito.utils import fetch_news
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def events(request):
    """Events for digital signage."""
    events = None
    photos = None
    earl = '{0}/live/json/events/group/screens/max/24/'.format(
        settings.LIVEWHALE_API_URL,
    )
    try:
        response = requests.get(earl,  timeout=10)
    except Exception:
        response = None
    if response:
        events = response.json()
        # images
        earl = '{0}/live/json/images/group/screens/tag/carthageviews/max/8/'.format(
            settings.LIVEWHALE_API_URL,
        )
        try:
            response = requests.get(earl,  timeout=10)
        except Exception:
            resposne = None
        if response:
            photos = response.json()
    return render(request, 'bridge/screens/events.html', {'events': events, 'photos': photos})


def news(request):
    """News for digital signage."""
    news = None
    photos = None
    earl = '{0}/live/json/news/group/screens/max/24/'.format(
        settings.LIVEWHALE_API_URL,
    )
    try:
        response = requests.get(earl,  timeout=10)
    except Exception:
        response = None
    if response:
        news = response.json()
        # images
        earl = '{0}/live/json/images/group/screens/tag/carthageviews/max/8/'.format(
            settings.LIVEWHALE_API_URL,
        )
        try:
            response = requests.get(earl,  timeout=10)
        except Exception:
            response = None
        if response:
            photos = response.json()
    return render(request, 'bridge/screens/news.html', {'news': news, 'photos': photos})
