from django.views.generic import ListView

from authorization.models import Permission

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

class PermissionListView(LoginRequiredMixin, ListView):
    model = Permission
    template_name = "permission/permission_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]

