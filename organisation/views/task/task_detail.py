from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.views.custom import SingleObjectView

from organisation.models import Task


class TaskDetailView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = Task
    template_name = "task/task_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
