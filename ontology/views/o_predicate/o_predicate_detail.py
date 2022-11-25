from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OPredicate


class OPredicateDetailView(CustomPermissionRequiredMixin, DetailView):
    model = OPredicate
    template_name = "o_predicate/o_predicate_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(OPredicateDetailView, self).get_context_data(**kwargs)
        predicate = context.get('object')
        model=predicate.model
        context['model_id'] = model.id
        return context