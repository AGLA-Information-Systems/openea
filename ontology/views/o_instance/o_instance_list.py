from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OInstance
from utils.views.custom import MultipleObjectsView

class OInstanceListView(CustomPermissionRequiredMixin, MultipleObjectsView, ListView):
    model = OInstance
    template_name = "o_instance/o_instance_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
    
    def get_queryset(self):
        concept_id=self.kwargs.get('concept_id')
        return OInstance.objects.filter(concept_id=concept_id)
