# -*- coding: utf-8 -*-

import argparse
import csv
import django
import sys

django.setup()

from djtito.catalog.models import Course


# set up command-line options
desc = """
    Accepts as input the name of the CSV file to import data.
    e.g. graduate.csv
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-f', '--file',
    required=True,
    help='CSV File name',
    dest='phile',
)


def main():
    """
    Shell script that manages data exported from Workday and imported into MySQL.

    Steps:

    1) execute destroy.py to dump the catalog.

    2) import the undergraduate courses:

    python courses.py --file=undergraduate.csv

    3) execute the following SQL incantation:

    update course_catalog set disc="" where dept="EDU";
    update course_catalog set disc="" where disc="MUS";
    update course_catalog set disc="" where disc="MGT";
    update course_catalog set disc="MED" where dept="EDU" and disc="EDU";
    update course_catalog set disc="EDU" where dept="EDU" and disc="";
    update course_catalog set disc="MMT" where dept="MUS" and disc="MUS";
    update course_catalog set disc="MUS" where dept="MUS" and disc="";
    update course_catalog set disc="MAT" where dept="ATH" and disc="ATH";
    update course_catalog set disc="BUS" where dept="MGT" and disc="";

    4) import the graduate courses:

    python courses.py --file=rgraduate.csv

    5) generate the PDF with the prince command:

    ssh eros.carthage.edu
    cd /d2/www/vhosts/carthage.edu/subdomains/eros/httpdocs/catalog/

    /usr/local/bin/prince \
    https://app.carthage.edu/djtito/catalog/print/ -o catalog.pdf

    6) optionally, set up a cronjob that runs every five minutes:

    */5 * * * * /usr/local/bin/prince https://app.carthage.edu/djtito/catalog/print/
    --output=/d2/www/vhosts/carthage.edu/subdomains/eros/httpdocs/catalog/catalog.pdf >> /dev/null 2>&1
    """
    with open(phile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:

            course = Course.objects.using('workday').create(
                title=row[0],
                dept=row[2],
                disc=row[2],
                crs_no=row[3],
                abstr=row[5],
            )
            print(course.crs_no, course.title)


if __name__ == '__main__':
    args = parser.parse_args()
    phile = args.phile
    sys.exit(main())
