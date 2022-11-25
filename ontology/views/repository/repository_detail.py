from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import Repository, OModel


class RepositoryDetailView(CustomPermissionRequiredMixin, DetailView):
    model = Repository
    template_name = "repository/repository_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(RepositoryDetailView, self).get_context_data(**kwargs)
        context['omodels'] = OModel.objects.filter(repository=context.get('object')).order_by('name').all()
        return context
