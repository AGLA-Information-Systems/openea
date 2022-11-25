from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from webapp.models import Organisation

class OrganisationDeleteView(CustomPermissionRequiredMixin, DeleteView):
    model = Organisation
    template_name = "organisation/organisation_delete.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

