from django import forms
from ontology.models import OReport, OReport, OModel

class OReportUpdateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea)
    model = forms.ModelChoiceField(queryset=OModel.objects.all())

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        super().__init__(*args, **kwargs)
        report = OReport.objects.get(id=initial_arguments.get('pk'))
        model = report.model
        
        self.fields['name'].initial = report.name
        self.fields['path'].initial = report.path
        self.fields['content'].initial = report.content
        self.fields['description'].initial = report.description
        self.fields['quality_status'].initial = report.quality_status
        self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model.id
        self.fields['model'].disabled = True

    class Meta:      
        model = OReport
        fields = ['name', 'description', 'path', 'content', 'model', 'quality_status',  'tags']
