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

from djtito.utils import create_archive, fetch_news, send_newsletter

from optparse import OptionParser

"""
Shell script that sends out email to students/faculty/staff
with news and events from LiveWhale data

Cron delivery for testing at:

Monday @ 7h
Wednesday @ 7h
Friday @ 7h
"""

# set up command-line options
desc = """
Accepts as input y or n, to send email to everybody or to
default, debug address.
"""

parser = OptionParser(description=desc)
parser.add_option("-s", "--send", help="Dry run or not? y/n.", dest="send")
parser.add_option("-d", "--days", help="Time frame in days.", dest="days")

def main():
    # fetch our stories
    data = fetch_news(days=days)
    # prepare template for static URLs without Analytics tracking
    data["static"] = True
    # create static file for archives
    data = create_archive(data)
    # send mail
    data["static"] = False
    data = send_newsletter(send, data)

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    send = options.send
    days = options.days

    if not send:
        print "'y' or 'n' as to whether or not this is a dry run.\n"
        parser.print_help()
        exit(-1)

    sys.exit(main())

