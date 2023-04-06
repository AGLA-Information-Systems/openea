from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OSlot
from utils.views.custom import MultipleObjectsView

class OSlotListView(CustomPermissionRequiredMixin, MultipleObjectsView, ListView):
    model = OSlot
    template_name = "o_slot/o_slot_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
