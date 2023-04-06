from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group

from organisation.models import Organisation

class OrganisationCreateView(CustomPermissionRequiredMixin, CreateView):
    model = Organisation
    fields = ['name', 'description', 'location']
    template_name = "organisation/organisation_create.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def get_initial(self):
        initials = super().get_initial()
        return initials

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        organisation = form.save()
        admin_group_name = organisation.name + 'Admin'
        org_admin_sec_group = create_organisation_admin_security_group(admin_security_group_name=admin_group_name, organisation=organisation)
        org_admin_sec_group.save()
        #form.save_m2m()
        return HttpResponseRedirect(self.success_url)
