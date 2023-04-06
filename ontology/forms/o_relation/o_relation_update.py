from django import forms
from django_select2 import forms as s2forms
from ontology.models import ORelation, ORelation, OModel
from taxonomy.models import Tag

class ORelationUpdateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea)
    model = forms.ModelChoiceField(queryset=OModel.objects.all())

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        super().__init__(*args, **kwargs)
        relation = ORelation.objects.get(id=initial_arguments.get('pk'))
        model = relation.model
        
        self.fields['name'].initial = relation.name
        self.fields['type'].initial = relation.type
        self.fields['description'].initial = relation.description
        self.fields['quality_status'].initial = relation.quality_status
        self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model.id
        self.fields['model'].disabled = True

    class Meta:      
        model = ORelation
        fields = ['name', 'description', 'type', 'model', 'quality_status',  'tags']
        widgets = {
            'type': s2forms.Select2Widget(),
            'tags': s2forms.ModelSelect2MultipleWidget(
                queryset=Tag.objects.all(),
                search_fields=['name__icontains']
            )
        }