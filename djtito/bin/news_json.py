# -*- coding: utf-8 -*-

import requests
import sys

from django.conf import settings
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CATEGORIES = [
    'Events|Top Stories',
    'Top Stories',
    'The Bridge: Campus News',
    'Academics|Innovation|The Bridge: Campus News',
    'Alumni News|The Bridge: Campus News',
    'Events|The Bridge: Lectures &amp; Presentations',
    'Community|Events|The Bridge: Lectures &amp; Presentations',
    'The Bridge: News for Students',
    'The Bridge: News for Faculty &amp; Staff',
    'The Bridge: Technology',
    'The Bridge: Kudos',
]


def main():
    for cat in CATEGORIES:
        cat_list = cat.split(':')
        if len(cat_list) > 0 and '|' not in cat_list[-1]:
            print(cat_list[-1].strip())
        else:
            print(cat_list[0].split('|')[-1])


    # https://www.carthage.edu/live/json/news/group/bridge/start_date/2023-08-11
    '''
    earl = '{0}/live/json/news/group/bridge/start_date/2023-08-11/category/The%20Bridge:%20Technology/'.format(
        settings.LIVEWHALE_API_URL,
    )
    print(earl)
    try:
        response = requests.get(earl,  timeout=10)
    except Exception as error:
        response = None
        print(error)

    if response:
        news = response.json()
        for story in news:
            print(story['thumbnail'])
    '''


if __name__ == '__main__':

    sys.exit(main())
