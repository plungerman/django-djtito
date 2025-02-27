# -*- coding: utf-8 -*-

import calendar
import collections
import datetime
import json
import logging
import os
import re
import requests

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from djtito.core.models import LivewhaleEvents as Events
from djtito.newsletter.forms import NewsletterForm
from djtito.utils import create_archive
from djtito.utils import fetch_events
from djtito.utils import fetch_news
from djtito.utils import send_newsletter
from djtools.decorators.auth import group_required


# django logging
logger = logging.getLogger('debug_logfile')


def archives(request, year=None):
    """
    Generates an ordered dictionary with a list of dictionaries.

    that contain information about the static files so that we
    can display the archives at the UI level in chronological order
    grouped by month.
    """
    now = datetime.datetime.now()
    philes_dict = collections.OrderedDict()
    # we set 'm' to numeric value of month to control
    # the display of month names
    mes = None
    month = None
    philes = []
    error = "No archives available for {0}".format(year)

    if not year:
        year = now.year
    ad = settings.ARCHIVES_DIR
    path = '{0}{1}{2}'.format(settings.STATIC_ROOT, ad, year)
    try:
        dir_list = sorted(os.listdir(path))
    except Exception:
        dir_list = None

    if dir_list:
        dir_list.reverse()
        for phile in dir_list:
            spliff = phile.split('_')
            # we only want .html files
            if spliff[1].split('.')[1] == 'html':
                if mes and spliff[0] != mes:
                    philes_dict[month] = philes
                    philes = []
                mes = spliff[0]
                month = calendar.month_name[int(mes)]
                path = '{0}{1}{2}/{3}'.format(
                    settings.STATIC_URL, ad, year, phile,
                )
                dayo = spliff[1].split('.')[0]
                date = datetime.datetime.strptime(
                    '{0}-{1}-{2}'.format(year, spliff[0], dayo), '%Y-%m-%d',
                )
                philes.append(
                    {'date': date, 'day': date.strftime('%A'), 'path': path},
                )

        if philes:
            philes_dict[month] = philes
    else:
        messages.add_message(
            request, messages.ERROR, error, extra_tags='danger',
        )
    # past year sub-nav
    past = []
    start = 2016
    today = datetime.date.today().year
    while start <= today:
        past.append(start)
        start += 1

    return render(
        request,
        'newsletter/archives_list.html',
        {'philes': philes_dict, 'year': year, 'pastnav': past},
    )


@group_required(settings.STAFF_GROUP)
def manager(request):
    """Newsletter manager for sending the email."""
    if request.GET.get('days'):
        days = int(request.GET.get('days'))
    else:
        days = ''
    newsletter = dict()
    # fetch our stories
    newsletter['news'] = fetch_news(days=days)
    # athletics events
    athletics_events = []
    bridge_events = []
    if settings.BRIDGE_EVENTS:
        events = fetch_events()
    newsletter['athletics_events'] = events['athletics']
    newsletter['bridge_events'] = events['bridge']
    # prepare template for static URLs without Analytics tracking
    newsletter['static'] = True
    if request.POST:
        balloons = request.POST.getlist('balloons')
        #logger.debug(request.POST)
        #logger.debug(balloons)
        form = NewsletterForm(request.POST)
        newsletter['news'] = fetch_news(balloons=balloons, days=days)
        if form.is_valid():
            cd = form.cleaned_data
            # prepare template for static URLs without Analytics tracking
            newsletter['static'] = True
            # create static file for archives
            newsletter = create_archive(newsletter)

            # send mail
            send = 'n'
            if cd['send_to'] == 'True':
                send = 'y'
            if days:
                days = '-d {0}'.format(days)
            newsletter['static'] = False
            newsletter['subject'] = cd['subject']
            newsletter = send_newsletter(send, newsletter)
            messages.add_message(
                request, messages.SUCCESS, 'Newsletter Sent', extra_tags='success',
            )
            return HttpResponseRedirect(reverse('newsletter_manager'))
    else:
        form = NewsletterForm()

    # we have to do this because of livewhale's broken database encoding
    template = loader.get_template('newsletter/manager.html')

    return HttpResponse(
        template.render(
            {'data': newsletter, 'form': form, 'days': days, 'balloons': True}, request,
        ),
        content_type='text/html; charset=utf8',
    )


@csrf_exempt
@group_required(settings.STAFF_GROUP)
def clear_cache(request, ctype='blurb'):
    """Clear the cache for API content."""
    if request.method == 'POST':
        cid = request.POST.get('cid')
        key = 'livewhale_{0}_{1}'.format(ctype, cid)
        cache.delete(key)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        earl = '{0}/live/{1}/{2}@JSON?cache={3}'.format(
            settings.LIVEWHALE_API_URL, ctype, cid, timestamp,
        )
        try:
            response = requests.get(earl, headers={'Cache-Control': 'no-cache'})
            text = json.loads(response.text)
            cache.set(key, text)
            body = mark_safe(text['body'])
        except Exception:
            body = ''
    else:
        body = "Requires AJAX POST"

    return HttpResponse(body, content_type='text/plain; charset=utf-8')
