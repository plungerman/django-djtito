# *- coding: utf-8 -*-

import collections
import datetime
import os
import sys

import django

django.setup()


from django.conf import settings
from djtito.core.models import CATEGORIES as cats
from djtito.core.models import LivewhaleNews as News


# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djtito.settings.shell')

django.setup()


def main():
    """Create static html file from newsletter content."""

    now = datetime.datetime.now()
    news = None
    day = now.strftime('%w')
    if day == '3' or day == '5':
        days = 3
    else:
        days = 4
    past = now - datetime.timedelta(days=int(days))
    news = News.objects.using('livewhale').filter(
        gid=settings.BRIDGE_GROUP,
    ).filter(status=1).filter(date_dt__lte=now).filter(
        is_archived__isnull=True,
    ).exclude(date_dt__lte=past)
    for story in news:
        kid = story.cat()
        print(kid)
        #print(story)
        if story.image():
            story.phile = '{0}.{1}'.format(
                story.image().filename,
                story.image().extension,
            )
        else:
            story.phile = None
        if kid:
            cats[kid][1].append(story)
    news = []
    for cat in cats:
        news.append(cats[cat])

    print(news)


if __name__ == '__main__':

    sys.exit(main())
