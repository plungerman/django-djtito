from django.conf import settings
from django.template import RequestContext, loader

from djwailer.core.models import LivewhaleNews as News
from djtools.utils.mail import send_mail

import datetime

NOW  = datetime.datetime.now()


def fetch_news(days=None):
    """
    1 Monday's Bridge newsletter includes everything posted on & since Friday.
    3 Wednesday's newsletter includes everything posted on and since Monday.
    5 Friday's newsletter includes everything posted on and since Wednesday.
    """


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


def send_newsletter(send, data):

    # mail stuff
    if send=="y":
        BCC = settings.NEWSLETTER_TO_LIST
        TO_LIST = ["bridge@carthage.edu",]
    else:
        BCC = settings.MANAGERS
        TO_LIST = settings.NEWSLETTER_TO_LIST_TEST

    FROM = "Carthage Bridge <bridge@carthage.edu>"
    subject = "[The Bridge] News & Events: {}".format(
        NOW.strftime("%A, %B %d, %Y")
    )

    # send mail
    request = None
    send_mail(
        request, TO_LIST, subject, FROM,
        "newsletter/email.html", data, BCC
    )

    return data


def create_archive(data):

    # create path to static file
    phile = "{}.html".format(NOW.strftime("%m_%d"))
    sendero = "{}{}{}/{}".format(
        settings.STATIC_ROOT, settings.ARCHIVES_DIR, NOW.year, phile
    )

    permalink = "https://{}{}{}{}/{}".format(
        settings.SERVER_URL, settings.STATIC_URL, settings.ARCHIVES_DIR,
        NOW.year, phile
    )

    # URL for 'read on website' link
    data["permalink"] = permalink
    # used in analytics tracking at the template level
    data["now"] = NOW
    # create static archive
    content = loader.render_to_string(
        'newsletter/archives.html', {"data":data,}
    ).encode("utf-8")
    with open(sendero, 'w') as static_file:
        static_file.write(content)

    return data
