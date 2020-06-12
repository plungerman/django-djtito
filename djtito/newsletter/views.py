import json
import os
import calendar
import datetime
import collections
import requests

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from djtito.newsletter.forms import NewsletterForm
from djtito.utils import create_archive, fetch_news, send_newsletter
from djtools.fields import TODAY
from djtools.decorators.auth import group_required
from djwailer.core.models import LivewhaleEvents as Events


def archives(request, year=None):
    """
    generates an ordered dictionary with a list of dictionaries
    that contain information about the static files so that we
    can display the archives at the UI level in chronological order
    grouped by month.
    """

    now  = datetime.datetime.now()
    dir_list = None
    philes_dict = collections.OrderedDict()
    # we set 'm' to numeric value of month to control
    # the display of month names
    m = None
    philes = []
    error = "No archives available for {}".format(year)

    if not year:
        year = now.year
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
                philes.append(
                    {'date':date,'day':date.strftime('%A'), 'path':path}
                )

        if philes:
            philes_dict[month] = philes

    else:
        messages.add_message(
            request, messages.ERROR, error, extra_tags='danger'
        )

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
    if request.GET.get('days'):
        days=int(request.GET.get('days'))
    else:
        days = ''
    # fetch our stories
    data = fetch_news(days=days)
    data['events'] = Events.objects.using('livewhale').filter(
        title__contains=' vs '
    ).exclude(title__contains='JV').filter(
        date_dt__gt=TODAY
    ).order_by('date_dt')[:10]
    # prepare template for static URLs without Analytics tracking
    data['static'] = True
    if request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # prepare template for static URLs without Analytics tracking
            data['static'] = True
            # create static file for archives
            data = create_archive(data)

            # send mail
            send = 'n'
            if cd['send_to'] == 'True':
                send = 'y'
            if days:
                days = '-d {}'.format(days)
            data['static'] = False
            data = send_newsletter(send, data)

            return HttpResponseRedirect(reverse('newsletter_manager'))
    else:
        form = NewsletterForm()

    # we have to do this because of livewhale's broken database encoding
    t = loader.get_template('newsletter/manager.html')

    return HttpResponse(
        t.render({'data': data,'form':form,'days':days,}, request),
        content_type='text/html; charset=utf8'
    )


@csrf_exempt
@group_required(settings.STAFF_GROUP)
def clear_cache(request, ctype='blurb'):
    if request.is_ajax() and request.method == 'POST':
        cid = request.POST.get('cid')
        key = 'livewhale_{0}_{1}'.format(ctype, cid)
        cache.delete(key)
        timestamp = date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        earl = '{}/live/{}/{}@JSON?cache={}'.format(
            settings.LIVEWHALE_API_URL,ctype,cid,timestamp
        )
        try:
            response = requests.get(earl, headers={'Cache-Control':'no-cache'})
            text = json.loads(response.text)
            cache.set(key, text)
            content = mark_safe(text['body'])
        except:
            content = ''
    else:
        content = "Requires AJAX POST"

    return HttpResponse(content, content_type='text/plain; charset=utf-8')
