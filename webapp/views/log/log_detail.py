from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from webapp.models import Log


class LogDetailView(CustomPermissionRequiredMixin, DetailView):
    model = Log
    template_name = "log/log_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
