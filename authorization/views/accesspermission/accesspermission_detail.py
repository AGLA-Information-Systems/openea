from django.views.generic import DetailView

from authorization.models import AccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

class AccessPermissionDetailView(LoginRequiredMixin, DetailView):
    model = AccessPermission
    template_name = "accesspermission/accesspermission_detail.html"
    accesspermission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
