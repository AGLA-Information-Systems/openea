from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.views import repository
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

from ontology.models import OModel

class OModelCreateView(CustomPermissionRequiredMixin, CreateView):
    model = OModel
    fields = ['name', 'version', 'description', 'repository',  'tags']
    template_name = "o_model/o_model_create.html"
    #success_url = reverse_lazy('o_model_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def get_initial(self):
        initials = super().get_initial()
        initials['repository'] = self.kwargs.get('repository_id')
        return initials

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance = OModel.get_or_create(name=form.cleaned_data['name'], version=form.cleaned_data['version'], description=form.cleaned_data['description'], repository=form.cleaned_data['repository'])
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['repository_id']
        return reverse('repository_detail', kwargs={'pk': pk})
