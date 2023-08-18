# -*- coding: utf-8 -*-

import csv
import django

django.setup()

from djtito.catalog.models import Course


with open('Course_Definitions_from_08_23_23.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)  # skip the headers
    for row in csv_reader:
        course_list = row[0].split('-')
        abstr = row[1]
        #print(abstr)
        title = course_list[-1].strip()
        #print(row[0])
        course_number = course_list[0]
        #print(course_number)
        dept = course_number.split(' ')[0][:3]
        #print(dept)
        course = Course.objects.using('workday').create(
            title=title,
            crs_no=course_number,
            abstr=abstr,
            dept=dept,
            disc=dept,
        )
        print(course)
