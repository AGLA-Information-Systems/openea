from django.http import Http404
from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import Repository, OModel
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class RepositoryDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = Repository
    template_name = "repository/repository_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(RepositoryDetailView, self).get_context_data(**kwargs)
        context['omodels'] = OModel.objects.filter(repository=context.get('object')).order_by('name').all()
        return context
