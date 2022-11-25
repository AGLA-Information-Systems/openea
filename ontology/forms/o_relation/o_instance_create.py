from django import forms
from ontology.controllers.knowledge_base import KnowledgeBaseController

from ontology.models import OConcept, OInstance, OModel, ORelation

class OInstanceCreateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False)
    concept = forms.ModelChoiceField(queryset=OConcept.objects.filter(model__id=1))
    #subjet = forms.ModelMultipleChoiceField(queryset=OConcept.objects.filter(model__id=1))
    #relation = forms.ModelChoiceField(queryset=ORelation.objects.filter(model__id=1))
    #object = forms.ModelChoiceField(queryset=OConcept.objects.filter(model__id=1))

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        concept_id = initial_arguments.get('concept_id')
        super().__init__(*args, **kwargs)
        class_ = OConcept.objects.get(id=concept_id)
        model = class_.model
        
        self.fields['concept'].queryset = OConcept.objects.filter(model__id=model.id).order_by('name')
        self.fields['concept'].initial = concept_id
        self.fields['model'].initial = model.id
        #for slot in KnowledgeBaseController.get_slots(model=model, instance=class_):


    class Meta:      
        model = OInstance
        fields = ['name', 'description', 'model', 'quality_status',  'tags']
