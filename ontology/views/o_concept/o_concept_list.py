from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OConcept
from openea.utils import Utils
from utils.views.custom import MultipleObjectsView

class OConceptListView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = OConcept
    template_name = "o_concept/o_concept_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]
