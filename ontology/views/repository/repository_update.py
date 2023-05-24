from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from ontology.forms.repository.repository_update import RepositoryUpdateForm

from ontology.models import Repository
from utils.views.custom import SingleObjectView

class RepositoryUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, UpdateView):
    model = Repository
    template_name = "repository/repository_update.html"
    form_class = RepositoryUpdateForm
    success_url = reverse_lazy('repository_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
    
    def get_initial(self):
        initials = super().get_initial()
        initials['pk'] = self.kwargs.get('pk')
        initials['organisation_ids'] = [x.organisation.id for x in self.request.user.profiles.all()]
        return initials

    def get_success_url(self):
        pk = self.object.id
        return reverse('repository_detail', kwargs={'pk': pk})