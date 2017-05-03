from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse

from djtito.newsletter.forms import NewsletterForm
from djtito.utils import create_archive, fetch_news, send_newsletter

from djtools.decorators.auth import group_required

import os
import calendar
import datetime
import collections


def archives(request, year=None):
    """
    generates an ordered dictionary with a list of dictionaries
    that contain information about the static files so that we
    can display the archives at the UI level in chronological order
    grouped by month.
    """

    NOW  = datetime.datetime.now()
    dir_list = None
    philes_dict = collections.OrderedDict()
    # we set 'm' to numeric value of month to control the display of month names
    m = None
    philes = []
    error = "No archives available for {}".format(year)

    if not year:
        year = NOW.year
    ad = settings.ARCHIVES_DIR
    path = '{}{}{}'.format(
        settings.STATIC_ROOT, ad, year
    )
    try:
        dir_list = sorted(os.listdir(path))
    except:
        pass

    if dir_list:
        dir_list.reverse()
        for f in dir_list:
            spliff = f.split('_')
            # we only want .html files
            if spliff[1].split('.')[1] == 'html':
                if m and spliff[0] != m:
                    philes_dict[month] = philes
                    philes = []
                m = spliff[0]
                month = calendar.month_name[int(m)]
                path = '{}{}{}/{}'.format(settings.STATIC_URL, ad, year, f)
                dayo = spliff[1].split('.')[0]
                date = datetime.datetime.strptime(
                    '{}-{}-{}'.format(year, spliff[0], dayo), '%Y-%m-%d'
                )
                philes.append({'date':date,'day':date.strftime("%A"), "path":path})

        if philes:
            philes_dict[month] = philes

    else:
        messages.add_message(request, messages.ERROR, error, extra_tags='danger')

    # past year sub-nav
    past = []
    start = 2016
    today = datetime.date.today().year
    while start <= today:
        past.append(start)
        start += 1

    return render(
        request, 'newsletter/archives_list.html',
        {'philes':philes_dict,'year':year,'pastnav':past}
    )


@group_required(settings.STAFF_GROUP)
def manager(request):
    data = None
    if request.GET.get("days"):
        days=int(request.GET.get("days"))
    else:
        days = ""
    # fetch our stories
    data = fetch_news(days=days)
    # prepare template for static URLs without Analytics tracking
    data["static"] = True
    if request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # prepare template for static URLs without Analytics tracking
            data["static"] = True
            # create static file for archives
            data = create_archive(data)

            # send mail
            send = "n"
            if cd["send_to"] == "True":
                send = "y"
            if days:
                days = "-d {}".format(days)
            data["static"] = False
            data = send_newsletter(send, data)

            return HttpResponseRedirect(reverse('newsletter_manager'))
    else:
        form = NewsletterForm()


    # we have to do this because of livewhale's broken database encoding
    t = loader.get_template('newsletter/manager.html')

    return HttpResponse(
        t.render({'data': data,'form':form,'days':days,}, request),
        content_type="text/html; charset=utf8"
    )
