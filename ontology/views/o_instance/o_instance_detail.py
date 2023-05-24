from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.controllers.utils import KnowledgeBaseUtils

from ontology.models import OInstance, OPredicate, ORelation, OSlot
from utils.views.custom import SingleObjectView


class OInstanceDetailView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, DetailView):
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
        inherited_predicates_as_subject = OPredicate.objects.filter(subject__in=lineage).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT).order_by('object').all()
        inherited_predicates_as_object = OPredicate.objects.filter(object__in=lineage).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT).order_by('subject').all()
        own_predicates_as_subject = OPredicate.objects.filter(subject=concept).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT).order_by('object').all()
        own_predicates_as_object = OPredicate.objects.filter(object=concept).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT).exclude(relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT).order_by('subject').all()

        all_predicates = [{'predicate':p, 
                           'kind':'inherited_as_subject', 
                           'sort_key':p.object.name, 
                           'slots': OSlot.objects.filter(model=model, predicate=p, subject=instance).all(),
                           'possible_concepts': [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=p.object)] + [p.object]} for p in inherited_predicates_as_subject] + \
                         [{'predicate':p,
                           'kind':'inherited_as_object',
                           'sort_key':p.subject.name,
                           'slots': OSlot.objects.filter(model=model, predicate=p, object=instance).all(),
                           'possible_concepts': [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=p.subject)] + [p.subject]} for p in inherited_predicates_as_object] + \
                         [{'predicate':p,
                           'kind':'own_as_subject',
                           'sort_key':p.object.name,
                           'slots':OSlot.objects.filter(model=model, predicate=p, subject=instance).all(),
                           'possible_concepts': [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=p.object)] + [p.object]} for p in own_predicates_as_subject] + \
                         [{'predicate':p,
                           'kind':'own_as_object',
                           'sort_key':p.subject.name,
                           'slots': OSlot.objects.filter(model=model, predicate=p, object=instance).all(),
                           'possible_concepts': [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=p.subject)] + [p.subject]} for p in own_predicates_as_object]
        context['all_predicates'] = sorted(all_predicates, key=lambda x: x['sort_key'])

        context['model_id'] = model.id
        return context
