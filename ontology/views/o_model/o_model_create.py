from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_model.o_model_create import OModelCreateForm
from ontology.models import OModel


class OModelCreateView(CustomPermissionRequiredMixin, CreateView):
    model = OModel
    template_name = "o_model/o_model_create.html"
    form_class = OModelCreateForm
    #success_url = reverse_lazy('o_model_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def get_initial(self):
        initials = super().get_initial()
        initials['repository'] = self.kwargs.get('repository_id')
        return initials

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance, created = OModel.objects.get_or_create(name=form.cleaned_data['name'],
                                                                version=form.cleaned_data['version'] or '1.0', 
                                                                repository=form.cleaned_data['repository'],
                                                                defaults={'description': form.cleaned_data['description'], 'created_by': self.request.user})
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        pk = self.kwargs['repository_id']
        return reverse('repository_detail', kwargs={'pk': pk})
