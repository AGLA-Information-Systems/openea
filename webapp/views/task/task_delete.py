from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin

from webapp.models import Task

class TaskDeleteView(LoginRequiredMixin, CustomPermissionRequiredMixin, DeleteView):
    model = Task
    template_name = "task/task_delete.html"
    success_url = reverse_lazy('task_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    # def get_success_url(self):
    #     pk = self.kwargs.get('organisation_id')
    #     return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})