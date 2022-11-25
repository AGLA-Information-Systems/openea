from django.views.generic import DetailView

from authorization.models import Permission
from authorization.controllers.utils import CustomPermissionRequiredMixin


class PermissionDetailView(CustomPermissionRequiredMixin, DetailView):
    model = Permission
    template_name = "permission/permission_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
