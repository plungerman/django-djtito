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
"""

def main():

    ad = settings.ARCHIVES_DIR

    path = "{}{}{}".format(
        settings.STATIC_ROOT, ad, NOW.year
    )
    dir_list = sorted(os.listdir(path))
    philes_dict = collections.OrderedDict()
    m = None
    for f in dir_list:
        spliff = f.split('_')
        if spliff[0] != m:
            if m:
                philes_dict[month] = philes
            philes = []
        m = spliff[0]
        if "0" in m:
            month = calendar.month_name[int(m[1:])]
        path = "{}{}{}/{}".format(settings.STATIC_URL, ad, NOW.year, f)
        dayo = spliff[1].split('.')[0]
        date = datetime.datetime.strptime('{}-{}-{}'.format(NOW.year,spliff[0],dayo), '%Y-%m-%d')
        print date.strftime("%A")
        philes.append({"dayo":dayo,"day":date.strftime("%A"), "path":path})

    philes_dict[month] = philes
    print philes_dict


######################
# shell command line
######################

if __name__ == "__main__":

    sys.exit(main())
