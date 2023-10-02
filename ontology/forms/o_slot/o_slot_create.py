from django import forms
from django_select2 import forms as s2forms

from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import OInstance, OModel, OPredicate, OSlot


class OSlotCreateForm(forms.ModelForm):
    new_object_name = forms.CharField(required=False)
    new_object_description = forms.CharField(required=False)
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
 
    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        is_subject = initial_arguments.get('is_subject')
        instance_id = initial_arguments.get('instance_id')
        predicate_id = initial_arguments.get('predicate_id')

        instance = OInstance.objects.get(id=instance_id)
        predicate = OPredicate.objects.get(id=predicate_id)
        model = instance.model
        super(OSlotCreateForm, self).__init__(*args, **kwargs)

        self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model.id
        self.fields['model'].disabled = True

        self.fields['predicate'].queryset = OPredicate.objects.filter(id=predicate.id)
        self.fields['predicate'].initial = initial_arguments.get('predicate_id')
        self.fields['predicate'].disabled = True
        
        possible_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=predicate.subject)] + [predicate.subject]
        queryset = OInstance.objects.filter(model__id=model.id, concept__in=possible_concepts).order_by('name')
        self.fields['subject'].widget = s2forms.ModelSelect2Widget(
            queryset=queryset,
            search_fields=['name__icontains']
        )
        self.fields['subject'].queryset = queryset
        
        possible_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=predicate.object)] + [predicate.object]
        queryset = OInstance.objects.filter(model__id=model.id, concept__in=possible_concepts).order_by('name')
        self.fields['object'].widget = s2forms.ModelSelect2Widget(
            queryset=queryset,
            search_fields=['name__icontains']
        )
        self.fields['object'].queryset = queryset

        if is_subject:
            self.fields['subject'].initial = instance.id
            self.fields['object'].required = False
        else:
            self.fields['object'].initial = instance.id
            self.fields['subject'].required = False
        
        
        self.fields['order'].initial = '0'
        
    class Meta:      
        model = OSlot
        fields = ['model', 'predicate', 'subject', 'object', 'description', 'order']
