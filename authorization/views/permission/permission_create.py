from utils.views.custom import CustomCreateView
from django.urls import reverse_lazy, reverse
from authorization.forms.permission.o_permission_create import OPermissionCreateForm

from authorization.models import Permission
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

class PermissionCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, CustomCreateView):
    model = Permission
    template_name = "permission/permission_create.html"
    form_class = OPermissionCreateForm
    #success_url = reverse_lazy('permission_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['user'] = self.request.user
        initials['organisation'] = self.kwargs.get('organisation_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})