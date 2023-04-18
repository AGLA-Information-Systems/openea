from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin


from ontology.models import Repository
from utils.views.custom import SingleObjectView

class RepositoryDeleteView(CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = Repository
    template_name = "repository/repository_delete.html"
    success_url = reverse_lazy('repository_list')
    permission_required = [('DELETE', model.get_object_type(), None)]
