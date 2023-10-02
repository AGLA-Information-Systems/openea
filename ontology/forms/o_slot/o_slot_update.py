from faulthandler import disable

from django import forms
from django_select2 import forms as s2forms

from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import (OConcept, OInstance, OModel, OPredicate,
                             ORelation, OSlot)


class OSlotUpdateForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=OInstance.objects.all())
    object = forms.ModelChoiceField(queryset=OInstance.objects.all())
    predicate = forms.ModelChoiceField(queryset=OPredicate.objects.all())
    model = forms.ModelChoiceField(queryset=OModel.objects.all())
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        slot_id = initial_arguments.get('slot_id')
        slot = OSlot.objects.get(id=slot_id)
        super().__init__(*args, **kwargs)

        self.fields['model'].queryset = OModel.objects.filter(id=slot.model.id)
        self.fields['model'].initial = slot.model.id
        self.fields['model'].disabled = True

        self.fields['predicate'].queryset = OPredicate.objects.filter(id=slot.predicate.id)
        self.fields['predicate'].initial = slot.predicate.id
        self.fields['predicate'].disabled = True

        self.fields['subject'].queryset = OInstance.objects.filter(id=slot.subject.id)
        self.fields['subject'].initial = slot.subject.id
        self.fields['subject'].disabled = True

        
        possible_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=slot.predicate.object)] + [slot.predicate.object]
        queryset = OInstance.objects.filter(model__id=slot.model.id, concept__in=possible_concepts).order_by('name')
        self.fields['object'].widget = s2forms.ModelSelect2Widget(
            queryset=queryset,
            search_fields=['name__icontains']
        )
        self.fields['object'].queryset = queryset
        self.fields['object'].initial = slot.object.id
        
        self.fields['order'].initial = slot.order

        self.fields['name'].initial = slot.name
        self.fields['description'].initial = slot.description

    class Meta:      
        model = OSlot
        fields = ['model', 'predicate', 'subject', 'object', 'description', 'order']
