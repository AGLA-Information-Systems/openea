from django import forms
from django_select2 import forms as s2forms
from authorization.models import Permission


class OPermissionCreateForm(forms.ModelForm):

    class Meta:
        model = Permission
        fields = ['action', 'object_type', 'object_identifier', 'description', 'organisation']
        widgets = {
            'action': s2forms.Select2Widget,
            'object_type': s2forms.Select2Widget,
        }