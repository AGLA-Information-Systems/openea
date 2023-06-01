from django import forms

from organisation.models import Profile


class ProfileCreateForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        super().__init__(*args, **kwargs)

        user_is_staff = initial_arguments.get('user_is_staff')
        if not user_is_staff:
            self.fields['user'].initial = initial_arguments.get('user_id')
            self.fields['user'].disabled = True

    class Meta:
        model = Profile
        fields = ['role', 'description', 'user', 'organisation']