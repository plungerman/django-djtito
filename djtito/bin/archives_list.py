# *- coding: utf-8 -*-

import argparse
import calendar
import collections
import datetime
import os
import sys

import django
from django.conf import settings

from djtools.fields import NOW


# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djtito.settings.shell')

django.setup()

# set up command-line options
desc = """
    generates an ordered dictionary with a list of dictionaries
    that contain information about the static files so that we
    can display the archives at the UI level
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-y',
    '--year',
    required=False,
    help="Year from which we want to display the archives.",
    dest='year',
)


def main():
    """Create static html file from newsletter content."""
    ad = settings.ARCHIVES_DIR

    path = '{0}{1}{2}'.format(settings.STATIC_ROOT, ad, year)
    dir_list = sorted(os.listdir(path))
    philes_dict = collections.OrderedDict()
    month = None
    philes = []
    for phile in dir_list:
        spliff = phile.split('_')
        if spliff[0] != month:
            if month:
                philes_dict[month] = philes
            philes = []
        month = spliff[0]
        if '0' in month:
            month = calendar.month_name[int(month[1:])]
        path = '{0}{1}{2}/{3}'.format(settings.STATIC_URL, ad, year, phile)
        dayo = spliff[1].split('.')[0]
        date = datetime.datetime.strptime(
            '{0}-{1}-{2}'.format(year, spliff[0], dayo), '%Y-%m-%d',
        )
        print(date.strftime('%A'))
        philes.append({'dayo': dayo, 'day': date.strftime('%A'), 'path': path})

    if philes:
        philes_dict[month] = philes

    print(philes_dict)


if __name__ == '__main__':

    args = parser.parse_args()
    year = args.year

    if not year:
        year = NOW.year

    sys.exit(main())
