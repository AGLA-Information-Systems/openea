from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from ontology.models import OConcept, OInstance
from utils.views.custom import SingleObjectView

class OInstanceDeleteView(CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = OInstance
    template_name = "o_instance/o_instance_delete.html"
    #success_url = reverse_lazy('o_instance_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})