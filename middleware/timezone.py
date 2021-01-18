import pytz

from django.utils import timezone
from urllib import parse
from datetime import datetime

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.COOKIES.get('timezone')
        if tzname:
            tz = pytz.timezone(parse.unquote(tzname))  # e.g. America/New York
            tz = datetime.now(tz).tzname()  # e.g. EST
            timezone.activate(tz)
        else:
            timezone.deactivate()
        return self.get_response(request)
