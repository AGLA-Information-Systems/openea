from django import forms
from django_select2 import forms as s2forms
from ontology.models import OConcept, OConcept, OModel
from taxonomy.models import Tag

class OConceptUpdateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea)
    model = forms.ModelChoiceField(queryset=OModel.objects.all())

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        super().__init__(*args, **kwargs)
        concept = OConcept.objects.get(id=initial_arguments.get('pk'))
        model = concept.model
        
        self.fields['name'].initial = concept.name
        self.fields['description'].initial = concept.description
        self.fields['quality_status'].initial = concept.quality_status
        self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model.id
        self.fields['model'].disabled = True

    class Meta:      
        model = OConcept
        fields = ['name', 'description', 'model', 'quality_status',  'tags']
        widgets = {
            'tags': s2forms.ModelSelect2MultipleWidget(
                queryset=Tag.objects.all(),
                search_fields=['name__icontains']
            )
        }
