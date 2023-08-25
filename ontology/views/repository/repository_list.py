from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import Repository
from openea.utils import Utils
from utils.views.custom import MultipleObjectsView

class RepositoryListView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = Repository
    template_name = "repository/repository_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]
