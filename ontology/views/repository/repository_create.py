import traceback
from utils.views.custom import CustomCreateView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from ontology.forms.repository.repository_create import RepositoryCreateForm

from ontology.models import Repository
from openea.utils import Utils
class RepositoryCreateView(LoginRequiredMixin, CustomCreateView):
    model = Repository
    template_name = "repository/repository_create.html"
    form_class = RepositoryCreateForm
    success_url = reverse_lazy('repository_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def form_valid(self, form):
        try:
            form.instance, created = Repository.objects.get_or_create(
                name=form.cleaned_data['name'],
                organisation=form.cleaned_data['organisation'],
                defaults={
                    'description': form.cleaned_data['description'],
                    'created_by': self.request.user
                })
        except Exception as e:
            traceback.print_exc()
            raise SuspiciousOperation(str(e))
        return HttpResponseRedirect(self.success_url)

    def get_initial(self):
        initials = super().get_initial()
        initials['organisation_id'] = self.kwargs.get('organisation_id') or self.request.user.active_profile.organisation.id
        initials['organisation_ids'] = [x.organisation.id for x in self.request.user.profiles.all()]
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('o_organisation_detail', kwargs={'pk': pk})
