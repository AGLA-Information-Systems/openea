from django.views.generic import DetailView

from configuration.models import Configuration
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

class ConfigurationDetailView(LoginRequiredMixin, DetailView):
    model = Configuration
    template_name = "configuration/configuration_detail.html"
    configuration_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
