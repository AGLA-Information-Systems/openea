from django.http import Http404
from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import ORelation
from utils.views.custom import SingleObjectView


class ORelationDetailView(CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = ORelation
    template_name = "o_relation/o_relation_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
   
    def get_context_data(self, **kwargs):
        context = super(ORelationDetailView, self).get_context_data(**kwargs)
        relation = context.get('object')
        model=relation.model
        context['model_id'] = model.id
        return context