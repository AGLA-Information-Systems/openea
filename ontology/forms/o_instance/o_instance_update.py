from django import forms
from django_select2 import forms as s2forms
from pagedown.widgets import PagedownWidget

from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import (OConcept, OInstance, OModel, OPredicate,
                             ORelation, OSlot)
from openea.utils import Utils


class OInstanceUpdateForm(forms.ModelForm):
    name = forms.CharField()
    code = forms.CharField(required=False)
    description = forms.CharField(required=False, widget=PagedownWidget)
    concept = forms.ModelChoiceField(queryset=OConcept.objects.all(), widget=s2forms.ModelSelect2Widget(
            queryset=OConcept.objects.all().order_by('name'),
            search_fields=['name__icontains']
        )
    )
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
        self.fields['quality_status'].initial = instance.quality_status
        self.fields['model'].queryset = OModel.objects.filter(id=model.id)
        self.fields['model'].initial = model.id
        self.fields['model'].disabled = True
        self.fields['concept'].queryset = OConcept.objects.filter(model__id=model.id)
        self.fields['concept'].widget.queryset = OConcept.objects.filter(model__id=model.id)
        self.fields['concept'].initial = concept.id
        #self.fields['concept'].disabled = True

        #self.fields['tag_groups'].initial = [tag_group.id for tag_group in instance.tag_groups.all()]
        #self.fields['tags'].queryset = Tag.objects.filter(tag_group__in=self.fields['tag_groups'].initial)
        #self.fields['tags'].initial = [tag.id for tag in instance.tags.all()]

        parents = KnowledgeBaseUtils.get_parent_concepts(concept=concept)
        lineage = [x[0] for x in parents] + [concept]
        # parents_and_own_predicates_as_subject = OPredicate.objects.filter(subject__in=lineage).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT)

        # for x in parents_and_own_predicates_as_subject:
        #     object_concept = x.object
        #     required = False
        #     if x.cardinality_min > 0:
        #         required = True
            
        #     slots = OSlot.objects.filter(model=model, predicate=x, subject=instance)
        #     if object_concept.name == Utils.RESOURCE_CONCEPT:
        #         for s in slots:
        #             self.fields[x.name] = forms.CharField(required=False)
        #             self.fields[x.name].initial = s.value
        #     else:
        #         self.fields[x.name] = forms.ModelMultipleChoiceField(queryset=OInstance.objects.filter(concept=object_concept), required=required)
        #         self.fields[x.name].initial = [s.object.id for s in slots if s.object is not None]

        # exclude inheritance relations
        for x in OPredicate.objects.filter(subject__in=lineage).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT):
            subject_concept = x.object
            required = False
            if x.cardinality_min > 0:
                required = True
            self.fields[x.name] = forms.ModelMultipleChoiceField(
                queryset=OInstance.objects.filter(concept=subject_concept),
                required=required, 
                widget=s2forms.ModelSelect2MultipleWidget(
                    queryset=OInstance.objects.filter(concept=subject_concept).order_by('name'),
                    search_fields=['name__icontains']
                )
            )
            slots = OSlot.objects.filter(model=model, predicate=x, subject=instance)
            self.fields[x.name].initial = [s.object.id for s in slots if s.object is not None]
            


            
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
        fields = ['name', 'description', 'code', 'concept', 'model', 'quality_status']
