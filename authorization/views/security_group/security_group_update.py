from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse

from authorization.models import SecurityGroup
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin

class SecurityGroupUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, UpdateView):
    model = SecurityGroup
    fields = ['name', 'description', 'organisation']
    template_name = "security_group/security_group_update.html"
    #success_url = reverse_lazy('security_group_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})