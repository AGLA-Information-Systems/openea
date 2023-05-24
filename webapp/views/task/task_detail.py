from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin

from webapp.models import Task


class TaskDetailView(LoginRequiredMixin, CustomPermissionRequiredMixin, DetailView):
    model = Task
    template_name = "task/task_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
