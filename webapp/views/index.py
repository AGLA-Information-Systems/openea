from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
import calendar
from calendar import HTMLCalendar
from ..forms import RegisterForm
from django.conf import settings
from .token import account_activation_token
 
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage


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

def register(request):
    if request.method == 'POST':  
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/")
    else:  
        form = RegisterForm()  
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    confirm = False 
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        confirm = True
    return render(request, 'registration/register_confirm.html', {'email': user.email, 'confirm': confirm})
