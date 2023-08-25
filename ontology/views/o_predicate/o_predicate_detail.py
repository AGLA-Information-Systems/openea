from django.http import Http404
from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OPredicate
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class OPredicateDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = OPredicate
    template_name = "o_predicate/o_predicate_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
  
    def get_context_data(self, **kwargs):
        context = super(OPredicateDetailView, self).get_context_data(**kwargs)
        predicate = context.get('object')
        model=predicate.model
        context['model_id'] = model.id
        return context