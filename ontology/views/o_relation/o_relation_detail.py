from django.http import Http404
from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import ORelation
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
        return context