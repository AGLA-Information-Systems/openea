from django import forms

from ontology.models import OReport, OReport, OModel
from taxonomy.models import Tag

class OReportCreateForm(forms.ModelForm):
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
        model = OReport
        fields = ['name', 'description', 'path', 'content', 'model', 'quality_status',  'tags']
