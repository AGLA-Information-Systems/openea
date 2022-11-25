from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import Repository

class RepositoryDeleteView(CustomPermissionRequiredMixin, DeleteView):
    model = Repository
    template_name = "repository/repository_delete.html"
    success_url = reverse_lazy('repository_list')
    permission_required = [('DELETE', model.get_object_type(), None)]
