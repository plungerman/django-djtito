from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

from djtito.newsletter import views
urlpatterns = [
    url(
        r'^archives/(?P<year>\d+)/$', views.archives, name='newsletter_archives'
    ),
    url(
        r'^archives/$', views.archives, name='newsletter_archives_default'
    ),
    url(
        r'^manager/$', views.manager, name='newsletter_manager'
    ),
    # clear livewhale blurb cache via ajax post
    url(
        '^cache/(?P<ctype>[-\w]+)/clear/', views.clear_cache, name='clear_cache'
    ),
    url(
        r'^$', RedirectView.as_view(url="/bridge/")
    ),
]
