from django.conf import settings

import os

days = 30
days = "-d 30"
send_to = "n"
x = "/usr/bin/python {}/bin/bridge_mail.py {} -s {}".format(
    settings.ROOT_DIR, days, send_to
)

print x

status = os.system( x )

print status
