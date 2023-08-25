from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from ontology.models import OConcept, OInstance
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class OInstanceDeleteView(LoginRequiredMixin, SingleObjectView, DeleteView):
    model = OInstance
    template_name = "o_instance/o_instance_delete.html"
    #success_url = reverse_lazy('o_instance_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.object.concept.id
        return reverse('o_concept_detail', kwargs={'pk': pk})