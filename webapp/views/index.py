from django.shortcuts import render
from datetime import date
import calendar
from calendar import HTMLCalendar
from django.conf import settings


def index(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    if year < 1900 or year > 2099:
        year = date.today().year
    month_name = calendar.month_name[month]
    title = "OpenEA - %s %s" % (month_name, year)
    cal = HTMLCalendar().formatmonth(year, month)
    return render(request, 'frontpage.'+settings.ENVIRONMENT+'.html', 
                  {'title': title,
                    'cal': cal,
                    'contact_email': settings.CONTACT_EMAIL})
