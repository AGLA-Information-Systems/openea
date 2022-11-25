from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import Repository

class RepositoryUpdateView(CustomPermissionRequiredMixin, UpdateView):
    model = Repository
    fields = ['name', 'description', 'organisation',  'tags']
    template_name = "repository/repository_update.html"
    success_url = reverse_lazy('repository_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
        return super().form_valid(form)
