from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.controllers.utils import KnowledgeBaseUtils

from ontology.models import OInstance, OPredicate, ORelation, OSlot
from utils.views.custom import SingleObjectView


class OInstanceDetailView(CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = OInstance
    template_name = "o_instance/o_instance_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
  
    def get_context_data(self, **kwargs):
        context = super(OInstanceDetailView, self).get_context_data(**kwargs)
        instance = context.get('object')
        model = instance.model
        concept = instance.concept

        lineage = [x[0] for x in KnowledgeBaseUtils.get_parent_concepts(concept=concept)]
        #print('LINEAGE', lineage)
        inherited_predicates_as_subject = OPredicate.objects.filter(subject__in=lineage).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT).all()
        inherited_predicates_as_object = OPredicate.objects.filter(object__in=lineage).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT).all()
        own_predicates_as_subject = OPredicate.objects.filter(subject=concept).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT).all()
        own_predicates_as_object = OPredicate.objects.filter(object=concept).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT).all()

        context['inherited_as_subject_slots'] = {}
        context['inherited_as_subject_possible_concepts'] = {}
        context['inherited_as_object_slots'] = {}
        context['inherited_as_object_possible_concepts'] = {}
        context['own_as_subject_slots'] = {}
        context['own_as_subject_possible_concepts'] = {}
        context['own_as_object_slots'] = {}
        context['own_as_object_possible_concepts'] = {}

        for p in inherited_predicates_as_subject:
            context['inherited_as_subject_slots'][p] = OSlot.objects.filter(model=model, predicate=p, subject=instance).all()
            context['inherited_as_subject_possible_concepts'][p.id] = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=p.object)] + [p.object]

        for p in inherited_predicates_as_object:
            context['inherited_as_object_slots'][p] = OSlot.objects.filter(model=model, predicate=p, object=instance).all()
            context['inherited_as_object_possible_concepts'][p.id] = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=p.subject)] + [p.subject]

        for p in own_predicates_as_subject:
            context['own_as_subject_slots'][p] = OSlot.objects.filter(model=model, predicate=p, subject=instance).all()
            context['own_as_subject_possible_concepts'][p.id] = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=p.object)] + [p.object]

        for p in own_predicates_as_object:
            context['own_as_object_slots'][p] = OSlot.objects.filter(model=model, predicate=p, object=instance).all()
            context['own_as_object_possible_concepts'][p.id] = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=p.subject)] + [p.subject]

        # print(context.get('ownslots'))
        # print(context.get('inslots'))
        # print(context.get('ownslots_possible_concepts'))
        context['model_id'] = model.id
        return context
