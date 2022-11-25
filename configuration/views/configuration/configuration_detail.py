from django.views.generic import DetailView

from configuration.models import Configuration
from authorization.controllers.utils import CustomPermissionRequiredMixin


class ConfigurationDetailView(CustomPermissionRequiredMixin, DetailView):
    model = Configuration
    template_name = "configuration/configuration_detail.html"
    configuration_required = [('VIEW', model.get_object_type(), None)]
