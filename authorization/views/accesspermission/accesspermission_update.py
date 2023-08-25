from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from authorization.forms.accesspermission.accesspermission_create import AccessPermissionCreateForm
from django.utils import timezone
from authorization.models import AccessPermission

from django.contrib.auth.mixins import LoginRequiredMixin

class AccessPermissionUpdateView(LoginRequiredMixin, UpdateView):
    model = AccessPermission
    template_name = "accesspermission/accesspermission_update.html"
    form_class = AccessPermissionCreateForm
    #success_url = reverse_lazy('accesspermission_list')
    accesspermission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})
