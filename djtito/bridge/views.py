# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.shortcuts import render
from djtito.core.models import LivewhaleEvents as Events
from djtito.core.models import LivewhaleNews as News
from djtito.utils import fetch_news


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

    return render(request, 'bridge/screens/news.html', {'news': news})
