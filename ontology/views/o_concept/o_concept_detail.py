from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import DetailView

from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import OConcept, OInstance
from utils.views.custom import SingleObjectView


class OConceptDetailView(CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = OConcept
    template_name = "o_concept/o_concept_detail.html"
    paginate_by = 10000
    permission_required = [('VIEW', model.get_object_type(), None)]
    
    def get_context_data(self, **kwargs):
        context = super(OConceptDetailView, self).get_context_data(**kwargs)
        concept = context.get('object')
        model=concept.model
        child_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=concept)]
        parent_concepts = [x[0] for x in KnowledgeBaseUtils.get_parent_concepts(concept=concept)]
        concepts = child_concepts + [concept]
        instance_list = OInstance.objects.filter(model=model, concept__in=concepts).order_by('name')
        instance_paginator = Paginator(instance_list, self.paginate_by)
        instance_page_number = self.request.GET.get('instance_page')
        context['parent_concepts'] = parent_concepts
        context['child_concepts'] = child_concepts
        context['instances'] = instance_paginator.get_page(instance_page_number)
        context['model_id'] = model.id
        return context
