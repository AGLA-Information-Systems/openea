from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin


from ontology.models import Repository
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class RepositoryDeleteView(LoginRequiredMixin, SingleObjectView, DeleteView):
    model = Repository
    template_name = "repository/repository_delete.html"
    success_url = reverse_lazy('repository_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]
