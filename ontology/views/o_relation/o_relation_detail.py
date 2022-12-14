from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import ORelation


class ORelationDetailView(CustomPermissionRequiredMixin, DetailView):
    model = ORelation
    template_name = "o_relation/o_relation_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(ORelationDetailView, self).get_context_data(**kwargs)
        relation = context.get('object')
        model=relation.model
        context['model_id'] = model.id
        return context