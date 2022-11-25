from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OModel

class OModelListView(CustomPermissionRequiredMixin, ListView):
    model = OModel
    template_name = "o_model/o_model_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
