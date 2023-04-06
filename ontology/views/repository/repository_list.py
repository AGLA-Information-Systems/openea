from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import Repository
from utils.views.custom import MultipleObjectsView

class RepositoryListView(CustomPermissionRequiredMixin, MultipleObjectsView, ListView):
    model = Repository
    template_name = "repository/repository_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
