# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.9/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djtito.settings")

import django
django.setup()

from django.conf import settings

from djtito.newsletter.views import fetch_news
from djtito.utils import create_archive

import argparse

"""
Create static html file from newsletter content
"""

# set up command-line options
desc = """
Accepts as input the number of days worth of stories to fetch
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-d", "--days",
    required=True,
    help="Time frame in days",
    dest="days"
)

def main():
    # mail stuff
    d = None
    if days:
        d = days
    data = fetch_news(days=d)
    data["static"] = True

    obj = create_archive(data)

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    days = args.days

    sys.exit(main())
