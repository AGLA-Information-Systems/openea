from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import Repository

class RepositoryListView(CustomPermissionRequiredMixin, ListView):
    model = Repository
    template_name = "repository/repository_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
