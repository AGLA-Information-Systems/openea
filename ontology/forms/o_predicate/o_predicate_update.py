from django import forms
from django_select2 import forms as s2forms

from ontology.models import OConcept, ORelation, OPredicate
from taxonomy.models import Tag


class OPredicateUpdateForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        predicate_id = initial_arguments.get('pk')
        predicate = OPredicate.objects.get(id=predicate_id)
        model_id = predicate.model.id
        super().__init__(*args, **kwargs)

        self.fields['subject'] = forms.ModelChoiceField(
            queryset=OConcept.objects.filter(model__id=model_id).order_by('name'),
            widget=s2forms.ModelSelect2Widget(
                queryset=OConcept.objects.filter(model__id=model_id).order_by('name'),
                search_fields=['name__icontains']
            ),
        )
        self.fields['subject'].initial=predicate.subject.id

        self.fields['relation'] = forms.ModelChoiceField(
            queryset=ORelation.objects.filter(model__id=model_id).order_by('name'),
            widget=s2forms.ModelSelect2Widget(
                queryset=ORelation.objects.filter(model__id=model_id).order_by('name'),
                search_fields=['name__icontains']
            ),
            initial=predicate.relation.id
        )
        self.fields['relation'].initial=predicate.relation.id

        self.fields['object'] = forms.ModelChoiceField(
            queryset=OConcept.objects.filter(model__id=model_id).order_by('name'),
            widget=s2forms.ModelSelect2Widget(
                queryset=OConcept.objects.filter(model__id=model_id).order_by('name'),
                search_fields=['name__icontains']
            ),
            initial=predicate.object.id
        )
        self.fields['object'].initial=predicate.object.id

        self.fields['model'].initial = model_id
        self.fields['model'].disabled = True
        self.fields['cardinality_min'].initial = predicate.cardinality_min
        self.fields['cardinality_max'].initial = predicate.cardinality_max

    class Meta:      
        model = OPredicate
        fields = ['model', 'subject', 'relation', 'object', 'description', 'cardinality_min', 'cardinality_max', 'quality_status',  'tags']
        widgets = {
            'tags': s2forms.ModelSelect2MultipleWidget(
                queryset=Tag.objects.all(),
                search_fields=['name__icontains']
            )
        }
