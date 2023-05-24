from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import Repository
from utils.views.custom import MultipleObjectsView

class RepositoryListView(LoginRequiredMixin, CustomPermissionRequiredMixin, MultipleObjectsView, ListView):
    model = Repository
    template_name = "repository/repository_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
