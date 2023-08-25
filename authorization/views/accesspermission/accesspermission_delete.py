from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from authorization.models import AccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils


class AccessPermissionDeleteView(LoginRequiredMixin, DeleteView):
    model = AccessPermission
    template_name = "accesspermission/accesspermission_delete.html"
    #success_url = reverse_lazy('accesspermission_list')
    accesspermission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})