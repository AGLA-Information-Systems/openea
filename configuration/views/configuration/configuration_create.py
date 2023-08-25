from utils.views.custom import CustomCreateView
from django.urls import reverse_lazy, reverse

from configuration.models import Configuration
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

class ConfigurationCreateView(LoginRequiredMixin, CustomCreateView):
    model = Configuration
    fields = ['action', 'object_type', 'object_identifier', 'description', 'organisation']
    template_name = "configuration/configuration_create.html"
    #success_url = reverse_lazy('configuration_list')
    configuration_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['user'] = self.request.user
        initials['organisation'] = self.kwargs.get('organisation_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})


class ConfigurationRebuildView(LoginRequiredMixin, CustomCreateView):
    model = Configuration