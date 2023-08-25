from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import ORelation
from openea.utils import Utils
from utils.views.custom import MultipleObjectsView

class ORelationListView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = ORelation
    template_name = "o_relation/o_relation_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]
