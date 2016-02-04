from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from djtools.utils.mail import send_mail
from djtools.decorators.auth import superuser_only

from djwailer.core.models import LivewhaleNews as News
from djtito.newsletter.forms import NewsletterForm

import os
import datetime
import uuid


def fetch_newsletter(days=None):
    """
    1 Monday's Bridge newsletter includes everything posted on & since Friday.
    3 Wednesday's newsletter includes everything posted on and since Monday.
    5 Friday's newsletter includes everything posted on and since Wednesday.
    """

    NOW  = datetime.datetime.now()

    TAGS = {
        498:['News & Notices',[]],
        499:['Lectures & Presentations',[]],
        500:['Arts & Performances',[]],
        477:['Kudos',[]],
        501:['Faculty & Staff News',[]],
        502:['Student News',[]],
        504:['Library & Technology',[]],
        912:['Top Bridge Stories',[]]
    }

    news = None
    # todays numeric value
    day = NOW.strftime("%w")
    # default number of days within which to fetch stories
    # is 4, unless wed or fri or we pass a value to this method
    if not days:
        if day == '3' or day == '5':
            days = 3
        else:
            days = 4

    past = NOW - datetime.timedelta(days=int(days))
    # fetch the news
    news = News.objects.using('livewhale').filter(
        gid=settings.BRIDGE_GROUP
    ).filter(status=1).filter(date_dt__lte=NOW).filter(
        is_archived__isnull=True
    ).exclude(date_dt__lte=past)

    for n in news:
        tid = n.tag(jid=True)
        if tid:
            TAGS[tid][1].append(n)
    news = []
    for t in TAGS:
        news.append(TAGS[t])
    return {'news':news}

@superuser_only
def manager(request):
    data = None
    if request.GET.get("days"):
        days=int(request.GET.get("days"))
    else:
        days = ""
    data = fetch_newsletter(days=days)
    data["cid"] = uuid.uuid4().int & (1<<64)-1
    data["now"] = datetime.datetime.now()
    form = NewsletterForm()
    if request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_to = "n"
            if cd["send_to"] == "True":
                send_to = "y"
            if days:
                days = "-d {}".format(days)
            # ok, don't even ask about this #chaputza. bloody livewhale.
            status = os.system(
                "/usr/bin/python {}/bin/bridge_mail.py {} -s {}".format (
                    settings.ROOT_DIR, days, send_to
                )
            )

            return HttpResponseRedirect(reverse('newsletter_manager'))

    t = loader.get_template('newsletter/manager.html')
    c = RequestContext(request, {'data': data,'form':form,'days':days,})

    return HttpResponse(
        t.render(c), content_type="text/html; charset=utf8"
    )

