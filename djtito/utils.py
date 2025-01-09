# -*- coding: utf-8 -*-

import copy
import datetime
import re
import requests

from django.conf import settings
from django.template import loader
from djtito.core.models import CATEGORIES
from djtito.core.models import LivewhaleNews as News
from djtools.utils.mail import send_mail
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fetch_events():
    """Obtain the calendar events from the CMS API."""
    events = {'athletics': [], 'bridge': []}

    # athletics events
    earl = '{0}/live/json/events/max/100/'.format(settings.LIVEWHALE_API_URL)
    try:
        response = requests.get(earl,  timeout=10)
    except Exception as error:
        response = None

    if response:
        sports = response.json()

    count = 0
    for event in sports:
        if ' vs ' in event['title'] and 'JV' not in event['title']:
            event['date_tito'] = datetime.datetime.strptime(event['date_iso'], "%Y-%m-%dT%H:%M:%S%z").date()
            events['athletics'].append(event)
            count += 1
        if count == 10:
            break

    # bridge calendar events
    earl = '{0}/live/json/events/group/bridge/max/25/'.format(settings.LIVEWHALE_API_URL)
    try:
        response = requests.get(earl,  timeout=10)
    except Exception as error:
        response = None

    if response:
        bridges = response.json()
    titles = []
    count = 0
    for event in bridges:
        title = re.sub(r'\W+', '', event['title'])
        if title not in titles:
            event['date_tito'] = datetime.datetime.strptime(event['date_iso'], "%Y-%m-%dT%H:%M:%S%z").date()
            events['bridge'].append(event)
            count += 1
        titles.append(title)
        if count == 10:
            break

    return events


def fetch_news(days=None):
    """
    Obtain the news items from the CMS API.

    1 Monday's Bridge newsletter includes everything posted on & since Friday.
    3 Wednesday's newsletter includes everything posted on and since Monday.
    5 Friday's newsletter includes everything posted on and since Wednesday.

    https://www.carthage.edu/live/json/news/group/bridge/start_date/2023-08-11
    "search_categories": "Events|The Bridge: Lectures &amp; Presentations",
    """
    cats = copy.deepcopy(CATEGORIES)
    days = None

    now = datetime.datetime.now()
    # today's numeric value for day of the week
    day = now.strftime('%w')
    if not days:
        if day == '3' or day == '5':
            days = 3
        else:
            days = 4

    past = now - datetime.timedelta(days=int(days))
    date = past.strftime('%Y-%m-%d')
    earl = '{0}/live/json/news/group/bridge/start_date/{1}/'.format(
        settings.LIVEWHALE_API_URL, date,
    )
    try:
        response = requests.get(earl,  timeout=10)
    except Exception as error:
        response = None

    news = []
    if response:
        news = response.json()
        # replace width and height with 100 and 67 respectiviely.
        # https://www.carthage.edu/live/image/gid/24/width/300/height/300/crop/1/src_region/0,0,993,636/32987_20_Feb-14_Lake_01.jpg
        for story in news:
            cat = story['news_categories']
            cat_list = cat.split(':')
            if len(cat_list) > 0 and '|' not in cat_list[-1]:
                cat = cat_list[-1].strip()
            else:
                cat = cat_list[0].split('|')[-1]
            cats[cat][1].append(story)
        news = []
        for cat, dic in cats.items():
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
    send_mail(
        None,
        to_list,
        subject,
        phrum,
        'newsletter/email.html',
        newsletter,
        reply_to=[phrum,],
        bcc=bcc,
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
