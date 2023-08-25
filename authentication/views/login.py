from authentication.forms.login import OrganisationLoginForm
from django.contrib.auth.views import LoginView


class OrganisationLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = OrganisationLoginForm
    success_url = 'HomePageView'