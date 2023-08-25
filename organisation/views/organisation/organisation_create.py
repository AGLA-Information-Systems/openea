from django.http import HttpResponseRedirect
from utils.views.custom import CustomCreateView
from django.urls import reverse_lazy
from authorization.controllers.utils import create_security_group_with_permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from organisation.models import Organisation
from openea.utils import Utils

class OrganisationCreateView(LoginRequiredMixin, CustomCreateView):
    model = Organisation
    fields = ['name', 'description', 'location']
    template_name = "organisation/organisation_create.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def get_initial(self):
        initials = super().get_initial()
        return initials

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        organisation = form.save()
        admin_group_name = organisation.name + ' ' + _('Admin')
        org_admin_sec_group = create_security_group_with_permissions(security_group_name=admin_group_name, organisation=organisation)
        org_admin_sec_group.save()
        #form.save_m2m()
        return HttpResponseRedirect(self.success_url)
