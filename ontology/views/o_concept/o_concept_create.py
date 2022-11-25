from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OConcept

class OConceptCreateView(CustomPermissionRequiredMixin, CreateView):
    model = OConcept
    fields = ['name', 'description', 'model', 'quality_status',  'tags']
    template_name = "o_concept/o_concept_create.html"
    #success_url = reverse_lazy('o_concept_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance = OConcept.get_or_create(model=form.cleaned_data['model'], name=form.cleaned_data['name'], description=form.cleaned_data['description'])
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('model_id')
        return reverse('o_model_detail', kwargs={'pk': pk})