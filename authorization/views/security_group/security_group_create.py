from unicodedata import name
from utils.views.custom import CustomCreateView
from django.urls import reverse_lazy, reverse

from authorization.models import SecurityGroup

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils


class SecurityGroupCreateView(LoginRequiredMixin, CustomCreateView):
    model = SecurityGroup
    fields = ['name', 'description', 'organisation']
    template_name = "security_group/security_group_create.html"
    #success_url = reverse_lazy('security_group_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

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

class SecurityGroupAdminCreateView(LoginRequiredMixin, CustomCreateView):
    model = SecurityGroup
    fields = ['name', 'description', 'organisation']
    template_name = "security_group/security_group_create.html"
    success_url = reverse_lazy('security_group_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def form_valid(self, form):
        raise NotImplementedError #TOFO Fix error
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
            create_security_group_with_permissions(organisation=None, security_group_name=form.cleaned_data['name'], superadmin=False)
        return super().form_valid(form)
    
    