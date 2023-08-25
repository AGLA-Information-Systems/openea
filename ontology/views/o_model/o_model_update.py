from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_model.o_model_update import OModelUpdateForm
from django.utils import timezone
from ontology.models import OModel
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class OModelUpdateView(LoginRequiredMixin, SingleObjectView, UpdateView):
    model = OModel
    form_class = OModelUpdateForm
    template_name = "o_model/o_model_update.html"
    #success_url = reverse_lazy('o_model_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.repository.id
        return reverse('repository_detail', kwargs={'pk': pk})