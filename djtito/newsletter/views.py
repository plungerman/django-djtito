from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse

from djtito.newsletter.forms import NewsletterForm
from djtito.utils import create_archive, fetch_news, send_newsletter
from djtools.decorators.auth import group_required


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
