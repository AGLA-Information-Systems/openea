from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from authorization.models import SecurityGroup
from authorization.controllers.utils import CustomPermissionRequiredMixin

class SecurityGroupDeleteView(CustomPermissionRequiredMixin, DeleteView):
    model = SecurityGroup
    template_name = "security_group/security_group_delete.html"
    #success_url = reverse_lazy('security_group_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})