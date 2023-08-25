from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _


class OrganisationLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username or email'), 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': _('Password'), 'id': 'password'}))
    organisation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Organisation'), 'id': 'organisation'}), required=False)
    
    def __init__(self, *args, **kwargs):
        super(OrganisationLoginForm, self).__init__(*args, **kwargs)
        self.fields['organisation'].widget.attrs.update(
        {'placeholder': 'Organisation', 'type': 'text', 'name': 'organisation', 'id': 'organisation'})
        self.fields['organisation'].label = 'Organisation'
        # self.helper = FormHelper()
        # self.helper.form_show_labels = False 


    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        organisation = self.cleaned_data.get("organisation")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password, organisation=organisation
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data