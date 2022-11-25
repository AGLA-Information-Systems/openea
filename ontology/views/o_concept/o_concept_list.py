from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OConcept

class OConceptListView(CustomPermissionRequiredMixin, ListView):
    model = OConcept
    template_name = "o_concept/o_concept_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
