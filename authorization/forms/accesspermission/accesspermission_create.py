from django import forms
from django_select2 import forms as s2forms
from authorization.models import AccessPermission, Permission


class AccessPermissionCreateForm(forms.ModelForm):

    class Meta:
        model = AccessPermission
        fields = ['permission', 'object_identifier', 'description', 'organisation']
        widgets = {
            'action': s2forms.Select2Widget,
            'object_type': s2forms.Select2Widget,
        }