from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OConcept
from utils.views.custom import MultipleObjectsView

class OConceptListView(CustomPermissionRequiredMixin, MultipleObjectsView, ListView):
    model = OConcept
    template_name = "o_concept/o_concept_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
