# -*- coding: utf-8 -*-

import collections
import copy
import datetime
import requests
import sys

from django.conf import settings
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# https://www.carthage.edu/live/json/news/group/bridge/start_date/2023-08-11
# https://www.carthage.edu/live/json/news/group/bridge/start_date/2025-01-06

CATEGORIES = collections.OrderedDict(
    {
        'Top Stories': ["Today's Top Stories", []],
        'Campus News': ['Other Campus News', []],
        'Lectures &amp; Presentations': ['Lectures & Presentations', []],
        'Arts': ['Arts', []],
        'News for Students': ['News for Students', []],
        'News for Faculty &amp; Staff': ['News for Faculty & Staff', []],
        'Technology': ['Technology', []],
        'Kudos': ['Kudos', []],
    },
)


def main():
    """Maquette for fetch news"""
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

    print(days)
    past = now - datetime.timedelta(days=int(days))
    date = past.strftime('%Y-%m-%d')
    print(date)
    earl = '{0}/live/json/news/group/bridge/start_date/{1}/'.format(
        settings.LIVEWHALE_API_URL, date,
    )
    print(earl)
    try:
        response = requests.get(earl,  timeout=10)
    except Exception as error:
        response = None
        print(error)

    news = []
    if response:
        news = response.json()
        for story in news:
            #print(story['thumbnail'])
            cat = story['news_categories']
            cat_list = cat.split(':')
            if len(cat_list) > 0 and '|' not in cat_list[-1]:
                #print(cat_list[-1].strip())
                cat = cat_list[-1].strip()
            else:
                #print(cat_list[0].split('|')[-1])
                cat = cat_list[0].split('|')[-1]
            cats[cat][1].append(story)
        news = []
        for cat, dic in cats.items():
            news.append(cats[cat])


        for new in news:
            print(new)


if __name__ == '__main__':

    sys.exit(main())
