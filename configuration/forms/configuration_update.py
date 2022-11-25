import json
from django import forms
from configuration.models import Configuration


from webapp.models import Organisation

class ConfigurationUpdateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False)
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all())

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        super().__init__(*args, **kwargs)
        configurations = Configuration.objects.get(id=initial_arguments.get('pk'))
        
        self.fields['name'].initial = configurations.name
        configurations_content = json.loads(configurations.content)
        for configuration, value in configurations_content:
            self.fields[configuration] = forms.CharField()
        self.fields['organisation'].queryset = Organisation.objects.filter(id=configurations.organisation.id)
        self.fields['organisation'].initial = configurations.organisation.id

    class Meta:      
        model = Configuration
        fields = ['name', 'content', 'organisation']

class ConfigurationMassUpdateForm(forms.ModelForm):
    value = forms.CharField(required=False)

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        super().__init__(*args, **kwargs)
        organisation = Organisation.objects.get(id=initial_arguments.get('pk'))
        configurations = Configuration.objects.filter(oragnisation=organisation)
        
        configurations_content = json.loads(configurations.content)
        for configuration, value in configurations_content:
            self.fields[configuration] = forms.CharField(initial=value)
            self.fields[configuration] = forms.CharField(initial=value)
            self.fields['organisation'].queryset = Organisation.objects.filter(id=configurations.organisation.id)
            self.fields['organisation'].initial = configurations.organisation.id

    class Meta:      
        model = Configuration
        fields = ['name', 'content', 'organisation']
