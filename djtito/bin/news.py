# -*- coding: utf-8 -*-

import copy
import datetime
import django
import re
import requests
import sys


django.setup()


from djtito.core.models import CATEGORIES
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
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
        #if day == '3' or day == '5':
        if day in ['2', '3', '4', '5']:
            days = 3
        else:
            days = 4
    print('days = {0}'.format(days))
    past = now - datetime.timedelta(days=int(days))
    date = past.strftime('%Y-%m-%d')
    earl = '{0}/live/json/news/group/bridge/start_date/{1}/'.format(
        django.conf.settings.LIVEWHALE_API_URL, date,
    )
    print(earl)
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
            cat = story.get('news_categories')
            if cat:
                cat_list = cat.split(':')
                if len(cat_list) > 0 and '|' not in cat_list[-1]:
                    cat = cat_list[-1].strip()
                else:
                    cat = cat.split('|')[1]
                thumb = story.get('thumbnail')
                story['news_categories'] = cat
                if story:
                    if thumb:
                        story['thumbnail'] = thumb.replace('width/300', 'width/100').replace('height/300/', '')
                    cats[cat][1].append(story)
        news = []
        from operator import itemgetter
        for cat, dic in cats.items():
            #print(cat)
            # reverse the order of the stories from how they are ordered in json API
            # sort top stories according to balloon sort order
            if cat == 'Top Stories':
                #top_sorted = [None] * len(cats[cat][1])
                #print(top_sorted)
                balloons = [2, 3, 1]
                print(balloons)
                print('cats')
                for counter, top in enumerate(cats[cat][1]):
                    print('{0}|{1}|{2}'.format(counter, cats[cat][1][counter]['id'], cats[cat][1][counter]['title']))
                print('ballon cats')
                for balloon in balloons:
                    print('{0}|{1}'.format(cats[cat][1][balloon - 1]['id'], cats[cat][1][balloon - 1]['title']))
                    top_sorted[balloon - 1] = cats[cat][1][balloon - 1]

                combined_lists = list(zip(balloons, cats[cat][1]))
                print(combined_lists)
                sorted_lists = sorted(combined_lists, key=lambda x: x[0])

                top_sorted = [item[1] for item in sorted_lists]
                print('top sorted')
                print(top_sorted)




                cats[cat][1] = top_sorted
            else:
                cats[cat][1] = list(reversed(cats[cat][1]))
            news.append(cats[cat])

    #for new in news:
        #print(news)
    #print({'news': news})


if __name__ == '__main__':
    sys.exit(main())
