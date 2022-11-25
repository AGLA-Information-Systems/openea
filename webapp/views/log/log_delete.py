from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from webapp.models import Log

class LogDeleteView(CustomPermissionRequiredMixin, DeleteView):
    model = Log
    template_name = "log/log_delete.html"
    success_url = reverse_lazy('log_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    # def get_success_url(self):
    #     pk = self.kwargs.get('organisation_id')
    #     return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})