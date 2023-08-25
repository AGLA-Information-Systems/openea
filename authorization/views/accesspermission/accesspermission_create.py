from utils.views.custom import CustomCreateView
from django.urls import reverse_lazy, reverse
from authorization.forms.accesspermission.accesspermission_create import AccessPermissionCreateForm

from authorization.models import AccessPermission

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils


class AccessPermissionCreateView(LoginRequiredMixin, CustomCreateView):
    model = AccessPermission
    template_name = "accesspermission/accesspermission_create.html"
    form_class = AccessPermissionCreateForm
    #success_url = reverse_lazy('accesspermission_list')
    accesspermission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

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