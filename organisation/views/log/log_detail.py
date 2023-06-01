from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from organisation.models import Log


class LogDetailView(LoginRequiredMixin, CustomPermissionRequiredMixin, DetailView):
    model = Log
    template_name = "log/log_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
