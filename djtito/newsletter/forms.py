# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings


SEND_TO = (
    ('', '---------'),
    (False, '[TEST] Communications'),
    (True, '[LIVE] Campus Community'),
)

if settings.DEBUG:
    REQ = {'class': 'required'}
else:
    REQ = {'class': 'required', 'required': 'required'}


class NewsletterForm(forms.Form):
    """Newsletter manager form for sending the newsletter via email."""

    send_to = forms.CharField(
        label="Send to",
        widget=forms.Select(choices=SEND_TO, attrs=REQ),
    )
    subject = forms.CharField(required=False)
