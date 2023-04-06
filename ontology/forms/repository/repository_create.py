from django import forms
from django_select2 import forms as s2forms

from ontology.models import Repository
from taxonomy.models import Tag
from organisation.models import Organisation


class RepositoryCreateForm(forms.ModelForm):
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all(), widget=s2forms.ModelSelect2Widget(
                queryset=Organisation.objects.all().order_by('name'),
                search_fields=['name__icontains']
            ))
    
    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        organisation_id = initial_arguments.get('organisation_id')
        organisation_ids = initial_arguments.get('organisation_ids')
        super().__init__(*args, **kwargs)
        organisation = Organisation.objects.get(id=organisation_id)

        self.fields['organisation'].queryset = Organisation.objects.filter(id__in=organisation_ids).order_by('name')
        self.fields['organisation'].widget.queryset = Organisation.objects.filter(id__in=organisation_ids).order_by('name')
        self.fields['organisation'].initial = organisation_id
        
    class Meta:
        model = Repository
        fields = ['name', 'description', 'organisation',  'tags']
        widgets = {
            'tags': s2forms.ModelSelect2MultipleWidget(
                queryset=Tag.objects.all(),
                search_fields=['name__icontains']
            )
        }