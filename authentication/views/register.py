from email.message import EmailMessage
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from authentication.token import account_activation_token
from authentication.forms.register import RegisterForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string  
from django.contrib.auth.models import User

class RegisterView(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if settings.ENVIRONMENT == 'xxx':
            if form.is_valid():  
                # save form in the memory not in database  
                user = form.save(commit=False)  
                user.is_active = False  
                user.save()  
                # to get the domain of the current site  
                current_site = get_current_site(request)  
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('registration/register_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token': account_activation_token.make_token(user),  
                })  
                to_email = form.cleaned_data.get('email')  
                email = EmailMessage( 
                    from_email=settings.EMAIL_HOST_USER, subject=mail_subject, body=message, to=[to_email]
                )  
                email.send()
                return render(request, 'registration/register_ask_confirmation.html', {'email': to_email})
        else:
            if form.is_valid():
                form.save()

                return HttpResponseRedirect("/")
        return render(request, 'registration/register.html', {'form': form})

    def get(self, request, *args, **kwargs):  
        form = RegisterForm()  
        return render(request, 'registration/register.html', {'form': form})
    
class ActivateView(View):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
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