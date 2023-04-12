from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OSlot
from utils.views.custom import MultipleObjectsView

class OSlotListView(LoginRequiredMixin, CustomPermissionRequiredMixin, MultipleObjectsView, ListView):
    model = OSlot
    template_name = "o_slot/o_slot_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
