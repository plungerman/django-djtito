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

import os
import django
import argparse
import datetime
import calendar
import collections

django.setup()

from django.conf import settings

from djtools.fields import NOW

"""
Create static html file from newsletter content
"""

# set up command-line options
desc = """
    generates an ordered dictionary with a list of dictionaries
    that contain information about the static files so that we
    can display the archives at the UI level
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-y", "--year",
    required=False,
    help="Year from which we want to display the archives.",
    dest="year"
)

def main():

    global year

    if not year:
        year = NOW.year

    ad = settings.ARCHIVES_DIR

    path = "{}{}{}".format(
        settings.STATIC_ROOT, ad, year
    )
    dir_list = sorted(os.listdir(path))
    philes_dict = collections.OrderedDict()
    m = None
    philes = []
    for f in dir_list:
        spliff = f.split('_')
        if spliff[0] != m:
            if m:
                philes_dict[month] = philes
            philes = []
        m = spliff[0]
        if "0" in m:
            month = calendar.month_name[int(m[1:])]
        path = "{}{}{}/{}".format(settings.STATIC_URL, ad, year, f)
        dayo = spliff[1].split('.')[0]
        date = datetime.datetime.strptime(
            '{}-{}-{}'.format(year,spliff[0],dayo), '%Y-%m-%d'
        )
        print date.strftime("%A")
        philes.append({"dayo":dayo,"day":date.strftime("%A"), "path":path})

    if philes:
        philes_dict[month] = philes

    print philes_dict


######################
# shell command line
######################

if __name__ == "__main__":

    args = parser.parse_args()
    year = args.year

    sys.exit(main())
