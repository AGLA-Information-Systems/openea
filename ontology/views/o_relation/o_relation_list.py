from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import ORelation

class ORelationListView(CustomPermissionRequiredMixin, ListView):
    model = ORelation
    template_name = "o_relation/o_relation_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
