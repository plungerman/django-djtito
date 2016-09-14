from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
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
    m = None
    philes = []
    error = "No archives available for {}".format(year)

    if not year:
        year = NOW.year
    ad = settings.ARCHIVES_DIR
    path = "{}{}{}".format(
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
            if spliff[1].split('.')[1] == "html":
                if spliff[0] != m:
                    if m:
                        philes_dict[month] = philes
                    philes = []
                m = spliff[0]
                if "0" in m:
                    month = calendar.month_name[int(m[1:])]
                path = "{}{}{}/{}".format(settings.STATIC_URL, ad, year, f)
                dayo = spliff[1].split('.')[0]
                date = datetime.datetime.strptime(
                    '{}-{}-{}'.format(year, spliff[0], dayo), '%Y-%m-%d'
                )
                philes.append({"date":date,"day":date.strftime("%A"), "path":path})

        if philes:
            philes_dict[month] = philes

    else:
        messages.add_message(request, messages.ERROR, error, extra_tags='danger')

    return render_to_response(
        "newsletter/archives_list.html", {"philes":philes_dict,"year":year},
        context_instance=RequestContext(request)
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


    t = loader.get_template('newsletter/manager.html')
    c = RequestContext(request, {'data': data,'form':form,'days':days,})

    return HttpResponse(
        t.render(c), content_type="text/html; charset=utf8"
    )
