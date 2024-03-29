from utils.views.custom import CustomCreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from organisation.models import Task
from openea.utils import Utils
class TaskCreateView(LoginRequiredMixin, CustomCreateView):
    model = Task
    fields = ['name', 'description', 'attachment', 'organisation']
    template_name = "task/task_create.html"
    #success_url = reverse_lazy('task_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['organisation'] = self.kwargs.get('organisation_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})