from django.http import HttpResponseBadRequest
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.views.custom import SingleObjectView
from organisation.models import Organisation

class OrganisationDeleteView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = Organisation
    template_name = "organisation/organisation_delete.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def form_valid(self, form):
        return HttpResponseBadRequest('OBJECT_IN_USE')

