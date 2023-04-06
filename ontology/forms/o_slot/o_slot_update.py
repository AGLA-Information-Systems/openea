from faulthandler import disable
from django import forms
from ontology.controllers.knowledge_base import KnowledgeBaseController

from ontology.models import OConcept, OInstance, OSlot, OModel, OPredicate, ORelation, OSlot

class OSlotUpdateForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=OInstance.objects.all())
    object = forms.ModelChoiceField(queryset=OInstance.objects.all())
    predicate = forms.ModelChoiceField(queryset=OPredicate.objects.all())
    model = forms.ModelChoiceField(queryset=OModel.objects.all())
    description = forms.CharField(required=False)

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        slot_id = initial_arguments.get('slot_id')

        slot = OSlot.objects.get(id=slot_id)
        instance = slot.subject
        predicate = slot.predicate
        model = slot.model
        super().__init__(*args, **kwargs)

        self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model.id
        self.fields['model'].disabled = True

        self.fields['predicate'].queryset = OPredicate.objects.filter(id=predicate.id)
        self.fields['predicate'].initial = predicate.id
        self.fields['predicate'].disabled = True

        self.fields['subject'].queryset = OInstance.objects.filter(id=instance.id)
        self.fields['subject'].initial = instance.id
        self.fields['subject'].disabled = True
        
        self.fields['object'].queryset = OInstance.objects.filter(model__id=model.id, concept=predicate.object)
        

    class Meta:      
        model = OSlot
        fields = ['model', 'predicate', 'subject', 'object', 'description']
