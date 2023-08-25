from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OPredicate
from openea.utils import Utils
from utils.views.custom import MultipleObjectsView

class OPredicateListView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = OPredicate
    template_name = "o_predicate/o_predicate_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]
