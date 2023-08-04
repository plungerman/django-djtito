# -*- coding: utf-8 -*-

import logging

from django import template
from django.core.cache import cache
from djtito.catalog.models import Course


logger = logging.getLogger('debug_logfile')
register = template.Library()


@register.tag()
def get_courses(parser, token):
    """{% get_courses as variable_name course_code %}"""
    bits = token.contents.split()
    logger.debug(bits)
    if len(bits) < 3:
        raise template.TemplateSyntaxError("'{0}' tag takes three arguments".format(bits[0]))
    if bits[1] != 'as':
        raise template.TemplateSyntaxError("First argument to '{0}' tag must be 'as'".format(bits[0]))
    return GetContent(bits)


class GetContent(template.Node):
    """Render the template tag at the UI level."""

    def __init__(self, bits):
        logger.debug(bits)
        self.varname = bits[2]
        self.code=bits[3]

    def render(self, context):
        """Obtain course data from database and expose to template layer."""
        code = self.code
        key = 'courses_{0}'.format(code)
        if cache.get(key):
            courses = cache.get(key)
        else:
            courses = Course.objects.using('workday').filter(disc=code)
            if courses:
                cache.set(key, courses)

        #context[self.varname] = _get_courses(self.code)
        context[self.varname] = courses
        return ''
