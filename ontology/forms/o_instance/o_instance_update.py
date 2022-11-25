from faulthandler import disable
from django import forms
from ontology.controllers.utils import KnowledgeBaseUtils

from ontology.models import OConcept, OInstance, OModel, OPredicate, OSlot
from taxonomy.models import Tag, TagGroup

class OInstanceUpdateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea)
    concept = forms.ModelChoiceField(queryset=OConcept.objects.all())
    model = forms.ModelChoiceField(queryset=OModel.objects.all())
    #tag_groups = forms.ModelMultipleChoiceField(required=False, queryset=TagGroup.objects.all())
    #tags = forms.ModelMultipleChoiceField(required=False, queryset=Tag.objects.filter(tag_group__in=[x.id for x in TagGroup.objects.all()]))

    def __init__(self,*args,**kwargs):
        initial_arguments = kwargs.pop('initial')
        super().__init__(*args, **kwargs)
        instance = OInstance.objects.get(id=initial_arguments.get('pk'))
        model = instance.model
        concept = instance.concept
        
        self.fields['name'].initial = instance.name
        self.fields['code'].initial = instance.code
        self.fields['description'].initial = instance.description
        self.fields['concept'].queryset = OConcept.objects.filter(model__id=model.id)
        self.fields['concept'].initial = concept
        self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model.id
        #self.fields['tag_groups'].initial = [tag_group.id for tag_group in instance.tag_groups.all()]
        #self.fields['tags'].queryset = Tag.objects.filter(tag_group__in=self.fields['tag_groups'].initial)
        #self.fields['tags'].initial = [tag.id for tag in instance.tags.all()]

        parents = KnowledgeBaseUtils.get_parent_concepts(concept=concept)
        lineage = [x[0] for x in parents] + [concept]
        parents_and_own_predicates_as_subject = OPredicate.objects.filter(subject__in=lineage)

        for x in parents_and_own_predicates_as_subject:
            if x.relation.name != "is-a":
                object_concept = x.object
                required = False
                if x.cardinality_min > 0:
                    required = True
                self.fields[x.name] = forms.ModelMultipleChoiceField(queryset=OInstance.objects.filter(concept=object_concept), required=required)
                slots = OSlot.objects.filter(model=model, predicate=x, subject=instance)
                self.fields[x.name].initial = [s.object.id for s in slots]

        # for x in predicates_as_object:
        #     subject_concept = x.subject
        #     required = False
        #     if x.cardinality_min > 0:
        #         required = True
        #     self.fields[x.name] = forms.ModelMultipleChoiceField(queryset=OInstance.objects.filter(concept=subject_concept), required=required)
        #     slots = OSlot.objects.filter(model=model, predicate=x, object=instance)
        #     self.fields[x.name].initial = [s.subject.id for s in slots]

        # rel_as_subject = [x for x in concept.is_subject_of.all()]
        # rel_as_object = [x for x in concept.is_object_of.all()]

        # for x in rel_as_subject:
        #     self.fields[x.name] = forms.ModelMultipleChoiceField(queryset=OConcept.objects.filter(pk__in=[]))
        # for x in rel_as_object:
        #     self.fields[x.name] = forms.ModelMultipleChoiceField(queryset=OConcept.objects.filter(model__id=1))


    class Meta:      
        model = OInstance
        fields = ['name', 'description', 'model', 'quality_status',  'tags']
