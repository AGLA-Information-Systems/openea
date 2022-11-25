from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
import calendar
from calendar import HTMLCalendar
from ..forms import RegisterForm
from django.conf import settings


def index(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    if year < 1900 or year > 2099:
        year = date.today().year
    month_name = calendar.month_name[month]
    title = "OpenEA - %s %s" % (month_name, year)
    cal = HTMLCalendar().formatmonth(year, month)
    return render(request, 'frontpage.'+settings.ENVIRONMENT+'.html', {'title': title, 'cal': cal, 'contact_email': settings.CONTACT_EMAIL})


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})