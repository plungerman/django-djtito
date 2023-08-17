# -*- coding: utf-8 -*-

import copy
import datetime
import requests

from django.conf import settings
from django.template import loader
from djtito.core.models import CATEGORIES
from djtito.core.models import LivewhaleNews as News
from djtools.utils.mail import send_mail


def fetch_news(days=None):
    """
    Obtain the news items from the CMS database.

    1 Monday's Bridge newsletter includes everything posted on & since Friday.
    3 Wednesday's newsletter includes everything posted on and since Monday.
    5 Friday's newsletter includes everything posted on and since Wednesday.

    https://www.carthage.edu/live/json/news/group/bridge/start_date/2023-08-11
    "search_categories": "Events|The Bridge: Lectures &amp; Presentations",
    """
    cats = copy.deepcopy(CATEGORIES)
    now = datetime.datetime.now()
    news = None
    # today's numeric value
    day = now.strftime('%w')
    # default number of days within which to fetch stories
    # is 4, unless wed or fri or we pass a value to this method
    if not days:
        if day == '3' or day == '5':
            days = 3
        else:
            days = 4

    past = now - datetime.timedelta(days=int(days))
    # fetch the news
    news = News.objects.using('livewhale').filter(
        gid=settings.BRIDGE_GROUP,
    ).filter(status=1).filter(date_dt__lte=now).filter(
        is_archived__isnull=True,
    ).exclude(date_dt__lte=past)

    for new in news:
        # [cid, name]
        if new.cat():
            kid = new.cat()[0]
            if new.image():
                new.phile = '{0}.{1}'.format(
                    new.image().filename,
                    new.image().extension,
                )
            else:
                new.phile = None
            if kid:
                cats[kid][1].append(new)
    news = []
    for cat in cats:
        news.append(cats[cat])
    return {'news': news}


def send_newsletter(send, newsletter):
    """Send the bridge newsletter."""
    # mail stuff
    if send == 'y':
        bcc = settings.NEWSLETTER_TO_LIST
        to_list = ['bridge@carthage.edu']
    else:
        bcc = settings.MANAGERS
        to_list = settings.NEWSLETTER_TO_LIST_TEST

    phrum = 'The Bridge <bridge@carthage.edu>'
    if newsletter['subject']:
        subject = newsletter['subject']
    else:
        subject = "[The Bridge] News & Events: {0}".format(
            datetime.datetime.now().strftime('%A, %B %d, %Y'),
        )

    # send mail
    request = None
    send_mail(
        request,
        to_list,
        subject,
        phrum,
        'newsletter/email.html',
        newsletter,
        bcc,
    )
    return newsletter


def create_archive(content_dict):
    """Create the archived file for each newsletter."""
    NOW = datetime.datetime.now()
    # suffix for file names
    suffix = NOW.strftime('%m_%d')
    # path to current directory
    path = '{0}{1}{2}'.format(
        settings.STATIC_ROOT, settings.ARCHIVES_DIR, NOW.year,
    )
    # fetch the banner image
    phile = '{0}.jpg'.format(suffix)
    sendero = '{0}/{1}'.format(path, phile)
    req = requests.get(settings.BRIDGE_NEWSLETTER_BANNER)
    with open(sendero, 'wb') as banner:
        banner.write(req.content)
    content_dict['banner'] = 'https://{0}{1}{2}{3}/{4}'.format(
        settings.SERVER_URL,
        settings.STATIC_URL,
        settings.ARCHIVES_DIR,
        NOW.year,
        phile,
    )
    # create path to static file
    phile = '{0}.html'.format(suffix)
    sendero = '{0}/{1}'.format(path, phile)
    permalink = 'https://{0}{1}{2}{3}/{4}'.format(
        settings.SERVER_URL,
        settings.STATIC_URL,
        settings.ARCHIVES_DIR,
        NOW.year,
        phile,
    )
    # URL for 'read on website' link
    content_dict['permalink'] = permalink
    # used in analytics tracking at the template level
    content_dict['now'] = NOW
    # create static archive
    newsletter = loader.render_to_string(
        'newsletter/archives.html', {'data': content_dict},
    )
    with open(sendero, 'w') as static_file:
        static_file.write(newsletter)

    return content_dict
