from django import forms
from django_select2 import forms as s2forms
from pagedown.widgets import PagedownWidget

from ontology.models import OConcept, OInstance, OModel


class OInstanceCreateForm(forms.ModelForm):
    name = forms.CharField()
    code = forms.CharField(required=False)
    description = forms.CharField(required=False, widget=PagedownWidget)
    concept = forms.ModelChoiceField(queryset=OConcept.objects.all(), widget=s2forms.ModelSelect2Widget(
                queryset=OConcept.objects.all().order_by('name'),
                search_fields=['name__icontains']
            ))

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        concept_id = initial_arguments.get('concept_id')
        super().__init__(*args, **kwargs)
        class_ = OConcept.objects.get(id=concept_id)
        model = class_.model

        self.fields['concept'].widget = s2forms.ModelSelect2Widget(
            queryset=OConcept.objects.filter(model__id=model.id).order_by('name'),
            search_fields=['name__icontains']
        )
        self.fields['concept'].queryset = OConcept.objects.filter(model__id=model.id).order_by('name')
        self.fields['concept'].widget.queryset = OConcept.objects.filter(model__id=model.id).order_by('name')
        self.fields['concept'].initial = concept_id

        self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model.id
        self.fields['model'].disabled = True


    class Meta:      
        model = OInstance
        fields = ['name', 'description', 'code', 'concept', 'model', 'quality_status']

