from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djtito.newsletter.views',
    url(
        r'^archives/(?P<cid>\d+)/$', 'archives', name='newsletter_archives'
    ),
    url(
        r'^archives/$', 'archives', name='newsletter_archives_default'
    ),
    url(
        r'^manager/$', 'manager', name='newsletter_manager'
    ),
    url(
        r'^$', RedirectView.as_view(url="/bridge/")
    ),
)
