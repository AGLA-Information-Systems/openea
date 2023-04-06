from django import forms
from django_select2 import forms as s2forms

from ontology.models import ORelation, ORelation, OModel
from taxonomy.models import Tag

class ORelationCreateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        model_id = initial_arguments.get('model_id')
        super().__init__(*args, **kwargs)
        model = OModel.objects.get(id=model_id)
        
        #self.fields['tags'].queryset = Tag.objects.filter(model__id=model.id).order_by('name')
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
            
