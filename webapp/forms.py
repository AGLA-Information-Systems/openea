
from django import forms
from django_select2 import forms as s2forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ontology.models import OConcept, OModel, OPredicate
from webapp.controllers.security import SecurityController
from webapp.constants import KNOWLEDGE_SET_CHOICES
from ontology.plugins import EXPORT_FORMAT_CHOICES, IMPORT_FORMAT_CHOICES

from organisation.models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


