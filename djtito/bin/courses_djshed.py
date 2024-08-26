# -*- coding: utf-8 -*-

import csv
import django


django.setup()


from djtito.catalog.models import Course
from djtito.schedule.models import Course as Schedule




#courses = Course.objects.using('workday').all()
#for course in courses:
    #shed = Schedule.object.filter(number=course.crs_no).filter(year='2024')


'''
title
credits
capacity
number
section
days
department
year
group
term
description
instructors
'''

missing = []
for shed in Schedule.objects.using('djshed').all().order_by('number'):
    #print(shed.number)
    try:
        course = Course.objects.using('workday').get(crs_no=shed.number)
        #print(course)
    except Exception:
        if shed.number not in missing:
            missing.append(shed.number)
            #print(shed.number)

for miss in missing:
    print(miss)

    '''
    if len(course) > 1:
        print(course)
    else:
        print('no course')
    '''

#    print(course.title)
#    print(course.time)

'''
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
'''
