from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OPredicate

class OPredicateListView(CustomPermissionRequiredMixin, ListView):
    model = OPredicate
    template_name = "o_predicate/o_predicate_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
