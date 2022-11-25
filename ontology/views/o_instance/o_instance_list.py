from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OInstance

class OInstanceListView(CustomPermissionRequiredMixin, ListView):
    model = OInstance
    template_name = "o_instance/o_instance_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
