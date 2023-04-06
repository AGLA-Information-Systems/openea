from django.http import Http404
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from ontology.models import ORelation
from utils.views.custom import SingleObjectView

class ORelationDeleteView(CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = ORelation
    template_name = "o_relation/o_relation_delete.html"
    #success_url = reverse_lazy('o_relation_list')
    permission_required = [('DELETE', model.get_object_type(), None)]
 
    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})
