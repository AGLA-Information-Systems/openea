from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils
from utils.views.custom import SingleObjectView

from organisation.models import Task


class TaskDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = Task
    template_name = "task/task_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
