from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from ontology.models import OModel
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class OModelDeleteView(LoginRequiredMixin, SingleObjectView, DeleteView):
    model = OModel
    template_name = "o_model/o_model_delete.html"
    #success_url = reverse_lazy('o_model_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]
 
    def get_success_url(self):
        pk = self.object.repository.id
        return reverse('repository_detail', kwargs={'pk': pk})