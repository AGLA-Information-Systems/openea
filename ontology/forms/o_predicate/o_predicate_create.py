from django import forms

from ontology.models import OConcept, ORelation, OPredicate

class OPredicateCreateForm(forms.ModelForm):
    #subjet = forms.ModelChoiceField(queryset=OConcept.objects.filter(model__id=1))
    #relation = forms.ModelChoiceField(queryset=ORelation.objects.filter(model__id=1))
    #object = forms.ModelChoiceField(queryset=OConcept.objects.filter(model__id=1))

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        model_id = initial_arguments.get('model')
        super().__init__(*args, **kwargs)

        self.fields['subject'].queryset = OConcept.objects.filter(model__id=model_id).order_by('name')
        self.fields['relation'].queryset = ORelation.objects.filter(model__id=model_id).order_by('name')
        self.fields['object'].queryset = OConcept.objects.filter(model__id=model_id).order_by('name')
        self.fields['model'].initial = model_id
        self.fields['cardinality_min'].initial = 0
        self.fields['cardinality_max'].initial = 0

    class Meta:      
        model = OPredicate
        fields = ['model', 'subject', 'relation', 'object', 'description', 'cardinality_min', 'cardinality_max', 'quality_status',  'tags']
