from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djtito.newsletter.views',
    url(
        r'^$', RedirectView.as_view(url="/bridge/")
    ),
    url(
        r'^manager/$', 'manager', name='newsletter_manager'
    ),
)
