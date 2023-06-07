from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from authorization.controllers.utils import (
    CustomPermissionRequiredMixin, create_organisation_admin_security_group)
from organisation.models import Organisation
from utils.views.custom import SingleObjectView


class OrganisationDeleteView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = Organisation
    template_name = "organisation/organisation_delete.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def form_valid(self, form):
        raise SuspiciousOperation('OBJECT_IN_USE')

