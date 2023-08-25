from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

from organisation.models import Log


class LogDetailView(LoginRequiredMixin, DetailView):
    model = Log
    template_name = "log/log_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
