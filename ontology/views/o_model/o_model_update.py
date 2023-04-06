from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.forms.o_model.o_model_update import OModelUpdateForm

from ontology.models import OModel
from utils.views.custom import SingleObjectView

class OModelUpdateView(CustomPermissionRequiredMixin, SingleObjectView, UpdateView):
    model = OModel
    form_class = OModelUpdateForm
    template_name = "o_model/o_model_update.html"
    #success_url = reverse_lazy('o_model_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.repository.id
        return reverse('repository_detail', kwargs={'pk': pk})