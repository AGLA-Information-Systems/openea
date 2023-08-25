from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from ontology.forms.repository.repository_update import RepositoryUpdateForm
from django.utils import timezone
from ontology.models import Repository
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class RepositoryUpdateView(LoginRequiredMixin, SingleObjectView, UpdateView):
    model = Repository
    template_name = "repository/repository_update.html"
    form_class = RepositoryUpdateForm
    success_url = reverse_lazy('repository_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_at = timezone.now()
        return super().form_valid(form)
    
    def get_initial(self):
        initials = super().get_initial()
        initials['pk'] = self.kwargs.get('pk')
        initials['organisation_ids'] = [x.organisation.id for x in self.request.user.profiles.all()]
        return initials

    def get_success_url(self):
        pk = self.object.id
        return reverse('repository_detail', kwargs={'pk': pk})