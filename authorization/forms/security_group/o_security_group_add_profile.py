from cProfile import Profile
from django import forms

from ontology.models import SecurityGroup

class SecurityGroupAddProfileForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        model_id = initial_arguments.get('model')
        super().__init__(*args, **kwargs)

        self.fields['profiles'].queryset = Profile.objects.filter(model__id=model_id)

    class Meta:      
        model = SecurityGroup
        fields = ['permission', 'profiles']
