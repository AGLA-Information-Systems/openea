from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from organisation.models import Organisation
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class OrganisationDeleteView(LoginRequiredMixin, SingleObjectView, DeleteView):
    model = Organisation
    template_name = "organisation/organisation_delete.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    def form_valid(self, form):
        raise SuspiciousOperation('OBJECT_IN_USE')

