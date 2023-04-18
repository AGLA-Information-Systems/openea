from django.http import Http404
from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import Repository, OModel
from utils.views.custom import SingleObjectView


class RepositoryDetailView(CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = Repository
    template_name = "repository/repository_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(RepositoryDetailView, self).get_context_data(**kwargs)
        context['omodels'] = OModel.objects.filter(repository=context.get('object')).order_by('name').all()
        return context
