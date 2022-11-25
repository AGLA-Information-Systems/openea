from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from authorization.models import Permission
from authorization.controllers.utils import CustomPermissionRequiredMixin

class PermissionDeleteView(CustomPermissionRequiredMixin, DeleteView):
    model = Permission
    template_name = "permission/permission_delete.html"
    #success_url = reverse_lazy('permission_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})