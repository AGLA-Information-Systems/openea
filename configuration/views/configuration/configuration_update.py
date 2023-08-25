from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from configuration.models import Configuration

from django.contrib.auth.mixins import LoginRequiredMixin

class ConfigurationUpdateView(LoginRequiredMixin, UpdateView):
    model = Configuration
    fields = ['action', 'object_type', 'object_identifier', 'description', 'organisation']
    template_name = "configuration/configuration_update.html"
    #success_url = reverse_lazy('configuration_list')
    configuration_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})