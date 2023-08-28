import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import DetailView
from authorization.models import Permission
from ontology.controllers.o_model import ModelUtils
from ontology.models import (OConcept, OInstance, OModel, OPredicate,
                             ORelation, OReport)
from ontology.plugins.json import GenericEncoder
from openea.utils import Utils
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class OModelDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = OModel
    template_name = "o_model/o_model_detail.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(OModelDetailView, self).get_context_data(**kwargs)
        model = context.get('object')
        
        context['show_concepts'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OConcept.get_object_type(), None))
        if context['show_concepts']:
            concept_list = OConcept.objects.filter(model=model).order_by('name').all()
            concept_paginator = Paginator(concept_list, self.paginate_by)
            concept_page_number = self.request.GET.get('concept_page')
            context['concepts'] = concept_paginator.get_page(concept_page_number)

        context['show_relations'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, ORelation.get_object_type(), None))
        if context['show_relations']:
            relation_list = ORelation.objects.filter(model=model).order_by('name').all()
            relation_paginator = Paginator(relation_list, self.paginate_by)
            relation_page_number = self.request.GET.get('relation_page')
            context['relations'] = relation_paginator.get_page(relation_page_number)

        context['show_predicates'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OPredicate.get_object_type(), None))
        if context['show_predicates']:
            predicate_list = OPredicate.objects.filter(model=model).order_by('object__name').order_by('relation__name').order_by('subject__name').all()
            predicate_paginator = Paginator(predicate_list, self.paginate_by)
            predicate_page_number = self.request.GET.get('predicate_page')
            context['predicates'] = predicate_paginator.get_page(predicate_page_number)

        context['show_instances'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OInstance.get_object_type(), None))
        if context['show_instances']:
            instance_list = OInstance.objects.filter(model=model).order_by('name').all()
            instance_paginator = Paginator(instance_list, self.paginate_by)
            instance_page_number = self.request.GET.get('instance_page')
            context['instances'] = instance_paginator.get_page(instance_page_number)

        context['show_reports'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OReport.get_object_type(), None))
        if context['show_reports']:
            report_list = OReport.objects.filter(model=model).order_by('name').all()
            report_paginator = Paginator(report_list, self.paginate_by)
            report_page_number = self.request.GET.get('report_page')
            context['reports'] = report_paginator.get_page(report_page_number)

        context['show_gap_analysis'] = True
        if context['show_gap_analysis']:
            # get all the models that are not the current one
            model_list = OModel.objects.exclude(id=model.id).order_by('name').all()
            model_paginator = Paginator(model_list, self.paginate_by)
            model_page_number = self.request.GET.get('model_page')
            context['models'] = model_paginator.get_page(model_page_number)

        context['show_all'] = context['show_predicates'] and context['show_concepts'] and context['show_instances']

        context['ontology_data'] = json.dumps(ModelUtils.ontology_to_dict(model=model), cls=GenericEncoder)

        return context
