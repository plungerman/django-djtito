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


def news(request):
    """News for digital signage."""
    days = 5
    # fetch our stories
    now = datetime.datetime.now()
    news = None
    # today's numeric value
    day = now.strftime('%w')
    past = now - datetime.timedelta(days=int(days))
    # fetch the news
    news = News.objects.using('livewhale').filter(
        gid=settings.BRIDGE_GROUP,
    ).filter(status=1).filter(date_dt__lte=now).filter(
        is_archived__isnull=True,
    ).exclude(date_dt__lte=past)
    # images
    # https://www.carthage.edu/live/json/images/group/screens/tag/carthageviews
    earl = '{0}/live/json/images/group/screens/tag/carthageviews'.format(
        settings.LIVEWHALE_API_URL,
    )
    response = requests.get(earl)
    jason = response.json()
    photos = jason

    return render(request, 'bridge/screens/news.html', {'news': news, 'photos': photos})
