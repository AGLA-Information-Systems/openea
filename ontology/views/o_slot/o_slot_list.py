from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OSlot
from openea.utils import Utils
from utils.views.custom import MultipleObjectsView

class OSlotListView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = OSlot
    template_name = "o_slot/o_slot_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]
