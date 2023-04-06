from django import forms
from django_select2 import forms as s2forms

from ontology.models import OConcept, OModel, ORelation, OPredicate
from taxonomy.models import Tag


class OPredicateCreateForm(forms.ModelForm):
    #subjet = forms.ModelChoiceField(queryset=OConcept.objects.filter(model__id=1))
    #relation = forms.ModelChoiceField(queryset=ORelation.objects.filter(model__id=1))
    #object = forms.ModelChoiceField(queryset=OConcept.objects.filter(model__id=1))

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        model_id = initial_arguments.get('model')
        super().__init__(*args, **kwargs)

        self.fields['subject'] = forms.ModelChoiceField(
            queryset=OConcept.objects.filter(model__id=model_id).order_by('name'),
            widget=s2forms.ModelSelect2Widget(
                queryset=OConcept.objects.filter(model__id=model_id).order_by('name'),
                search_fields=['name__icontains']
            )
        )
        self.fields['relation'] = forms.ModelChoiceField(
            queryset=ORelation.objects.filter(model__id=model_id).order_by('name'),
            widget=s2forms.ModelSelect2Widget(
                queryset=ORelation.objects.filter(model__id=model_id).order_by('name'),
                search_fields=['name__icontains']
            )
        )
        self.fields['object'] = forms.ModelChoiceField(
            queryset=OConcept.objects.filter(model__id=model_id).order_by('name'),
            widget=s2forms.ModelSelect2Widget(
                queryset=OConcept.objects.filter(model__id=model_id).order_by('name'),
                search_fields=['name__icontains']
            )
        )

        #self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model_id
        self.fields['model'].disabled = True
        self.fields['cardinality_min'].initial = 0
        self.fields['cardinality_max'].initial = 0

    class Meta:      
        model = OPredicate
        fields = ['model', 'subject', 'relation', 'object', 'description', 'cardinality_min', 'cardinality_max', 'quality_status',  'tags']
        widgets = {
            'tags': s2forms.ModelSelect2MultipleWidget(
                queryset=Tag.objects.all(),
                search_fields=['name__icontains']
            )
        }