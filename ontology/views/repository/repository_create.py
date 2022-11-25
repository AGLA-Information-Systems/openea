from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import Repository

class RepositoryCreateView(CustomPermissionRequiredMixin, CreateView):
    model = Repository
    #fields = '__all__'
    fields = ['name', 'description', 'organisation',  'tags']
    template_name = "repository/repository_create.html"
    success_url = reverse_lazy('repository_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance = Repository.get_or_create(name=form.cleaned_data['name'], organisation=form.cleaned_data['organisation'], description=form.cleaned_data['description'])
            form.instance.created_by = self.request.user
        return super().form_valid(form)
