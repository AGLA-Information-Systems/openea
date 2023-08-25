from django.views.generic import DetailView

from authorization.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

class PermissionDetailView(LoginRequiredMixin, DetailView):
    model = Permission
    template_name = "permission/permission_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
