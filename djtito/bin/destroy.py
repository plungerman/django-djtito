# -*- coding: utf-8 -*-

import django

django.setup()

from djtito.catalog.models import Course

#for course in Course.objects.using('workday').all():
#    print(course.title)

# delete the current catalog of courses
Course.objects.using('workday').all().delete()
