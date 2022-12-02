# -*- coding: utf-8 -*-

from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    crs_no = models.CharField(max_length=128, blank=True, null=True)
    abstr = models.TextField(blank=True, null=True)
    cat = models.CharField(max_length=8, blank=True, null=True)
    dept = models.CharField(max_length=8, blank=True, null=True)
    disc = models.CharField(max_length=8, blank=True, null=True)
    min_hrs = models.FloatField(blank=True, null=True)
    max_hrs = models.FloatField(blank=True, null=True)
    credits = models.CharField(max_length=8, blank=True, null=True)
    sess = models.CharField(max_length=4, blank=True, null=True)
    txt = models.CharField(max_length=64, blank=True, null=True)
    terms = models.CharField(max_length=128, blank=True, null=True)
    firstname = models.CharField(max_length=32, blank=True, null=True)
    middlename = models.CharField(max_length=32, blank=True, null=True)
    lastname = models.CharField(max_length=64, blank=True, null=True)
    suffixname = models.CharField(max_length=32, blank=True, null=True)
    fac_id = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    instructors = models.CharField(max_length=1024, blank=True, null=True)
    core = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'course_catalog'
