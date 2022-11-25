from unicodedata import name
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.controllers.knowledge_base import KnowledgeBaseController
from ontology.forms.o_instance.o_instance_create import OInstanceCreateForm
from django.views.generic.edit import FormView

from ontology.models import OConcept, OInstance, OModel

class OInstanceCreateView(CustomPermissionRequiredMixin, FormView):
    model = OInstance
    template_name = "o_instance/o_instance_create.html"
    form_class = OInstanceCreateForm
    #success_url = reverse_lazy('o_instance_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            concept = OConcept.objects.get(id=self.kwargs.get('concept_id'))
            model = concept.model
            concept = form.cleaned_data['concept']
            form.instance = OInstance.get_or_create(model=model, concept=concept, name=form.cleaned_data['name'], code=form.cleaned_data['code'], description=form.cleaned_data['description'])
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['concept_id'] = self.kwargs.get('concept_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('concept_id')
        return reverse('o_concept_detail', kwargs={'pk': pk})