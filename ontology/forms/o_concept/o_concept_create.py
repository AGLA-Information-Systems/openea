from django import forms
from ontology.controllers.knowledge_base import KnowledgeBaseController

from ontology.models import OConcept, OConcept, OModel, ORelation
from taxonomy.models import Tag

class OConceptCreateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False)

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        concept_id = initial_arguments.get('concept_id')
        super().__init__(*args, **kwargs)
        class_ = OConcept.objects.get(id=concept_id)
        model = class_.model
        
        self.fields['tags'].queryset = Tag.objects.filter(model__id=model.id).order_by('name')
        self.fields['concept'].initial = concept_id
        self.fields['model'].initial = model.id


    class Meta:      
        model = OConcept
        fields = ['name', 'description', 'model', 'quality_status',  'tags']
