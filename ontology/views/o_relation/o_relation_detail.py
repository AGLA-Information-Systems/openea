from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import DetailView

from ontology.models import OPredicate, ORelation
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class ORelationDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = ORelation
    template_name = "o_relation/o_relation_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
   
    def get_context_data(self, **kwargs):
        context = super(ORelationDetailView, self).get_context_data(**kwargs)
        relation = context.get('object')
        model=relation.model
        context['model_id'] = model.id
        context['predicates'] = OPredicate.objects.filter(model=model, relation=relation).order_by('subject__name').order_by('object__name')
        return context