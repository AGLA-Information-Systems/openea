from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, create_organisation_admin_security_group

from webapp.models import Organisation

class OrganisationCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, CreateView):
    model = Organisation
    fields = ['name', 'description', 'location']
    template_name = "organisation/organisation_create.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def get_initial(self):
        initials = super().get_initial()
        #initials['repository'] = self.kwargs.get('repository_id')
        return initials

    def form_valid(self, form):
        if self.request.user.is_active:
            form.instance.created_by = self.request.user
            organisation = form.save(commit=False)
            admin_group_name = organisation.name + 'Admin'
            org_admin_sec_group = create_organisation_admin_security_group(admin_security_group_name=admin_group_name, organisation=organisation)
            organisation.save()
            form.save_m2m()
        return HttpResponseRedirect(self.success_url)
