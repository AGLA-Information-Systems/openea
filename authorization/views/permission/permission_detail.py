from django.views.generic import DetailView

from authorization.models import Permission
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin


class PermissionDetailView(LoginRequiredMixin, CustomPermissionRequiredMixin, DetailView):
    model = Permission
    template_name = "permission/permission_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
