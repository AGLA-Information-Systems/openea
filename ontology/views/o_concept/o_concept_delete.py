from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.models import OConcept
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class OConceptDeleteView(LoginRequiredMixin, SingleObjectView, DeleteView):
    model = OConcept
    template_name = "o_concept/o_concept_delete.html"
    #success_url = reverse_lazy('o_concept_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})