from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from webapp.models import Task


class TaskDetailView(CustomPermissionRequiredMixin, DetailView):
    model = Task
    template_name = "task/task_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
