from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils
from utils.views.custom import SingleObjectView

from organisation.models import Task

class TaskDeleteView(LoginRequiredMixin, SingleObjectView, DeleteView):
    model = Task
    template_name = "task/task_delete.html"
    success_url = reverse_lazy('task_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    # def get_success_url(self):
    #     pk = self.kwargs.get('organisation_id')
    #     return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})