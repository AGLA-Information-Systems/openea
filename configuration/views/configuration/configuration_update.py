from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from datetime import datetime
from configuration.models import Configuration
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

class ConfigurationUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, UpdateView):
    model = Configuration
    fields = ['action', 'object_type', 'object_identifier', 'description', 'organisation']
    template_name = "configuration/configuration_update.html"
    #success_url = reverse_lazy('configuration_list')
    configuration_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_at = datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})