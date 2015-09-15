from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('',
    # auth
    url(
        r'^accounts/login/$',auth_views.login,
        {'template_name': 'accounts/login.html'},name='auth_login'
    ),
    url(
        r'^accounts/logout/$',auth_views.logout,
        {'next_page': '/djtito/accounts/loggedout/'}
    ),
    url(
        r'^accounts/loggedout/',loggedout,
        {'template_name': 'accounts/logged_out.html'}
    ),
    url(
        r'^accounts/$',
        RedirectView.as_view(url='/djtito/accounts/login/')
    ),
    #admin
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    # bridge
    url(
        r'^newsletter/',
        include('djtito.newsletter.urls')
    ),
    url(
        r'^$',
        RedirectView.as_view(url="/djtito/newsletter/manager/")
    ),
)
