from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import ORelation

class ORelationUpdateView(CustomPermissionRequiredMixin, UpdateView):
    model = ORelation
    fields = ['name', 'description', 'type', 'model', 'quality_status',  'tags']
    template_name = "o_relation/o_relation_update.html"
    #success_url = reverse_lazy('o_relation_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})