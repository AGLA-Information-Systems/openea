from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OConcept, OSlot

class OSlotDeleteView(CustomPermissionRequiredMixin, DeleteView):
    model = OSlot
    template_name = "o_slot/o_slot_delete.html"
    #success_url = reverse_lazy('o_slot_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})