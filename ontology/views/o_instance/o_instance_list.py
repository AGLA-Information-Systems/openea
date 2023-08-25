from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OInstance
from openea.utils import Utils
from utils.views.custom import MultipleObjectsView

class OInstanceListView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = OInstance
    template_name = "o_instance/o_instance_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]
    
    def get_queryset(self):
        concept_id=self.kwargs.get('concept_id')
        return OInstance.objects.filter(concept_id=concept_id)
