from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from ontology.models import OModel
from utils.views.custom import SingleObjectView

class OModelDeleteView(CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = OModel
    template_name = "o_model/o_model_delete.html"
    #success_url = reverse_lazy('o_model_list')
    permission_required = [('DELETE', model.get_object_type(), None)]
 
    def get_success_url(self):
        pk = self.object.repository.id
        return reverse('repository_detail', kwargs={'pk': pk})