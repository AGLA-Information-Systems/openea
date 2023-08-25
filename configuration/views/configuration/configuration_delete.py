from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from configuration.models import Configuration
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils


class ConfigurationDeleteView(LoginRequiredMixin, DeleteView):
    model = Configuration
    template_name = "configuration/configuration_delete.html"
    #success_url = reverse_lazy('configuration_list')
    configuration_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})