from unicodedata import name

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from authorization.controllers.utils import CustomPermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_instance.o_instance_create import OInstanceCreateForm
from ontology.models import OConcept, OInstance, OModel


class OInstanceCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, FormView):
    model = OInstance
    template_name = "o_instance/o_instance_create.html"
    form_class = OInstanceCreateForm
    #success_url = reverse_lazy('o_instance_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        concept = OConcept.objects.get(id=self.kwargs.get('concept_id'))
        model = concept.model
        concept = form.cleaned_data['concept']
        #form.instance = OInstance.get_or_create(model=model, concept=concept, name=form.cleaned_data['name'], code=form.cleaned_data['code'], description=form.cleaned_data['description'])
        form.instance.instance, created = OInstance.objects.get_or_create(model=model,
                                                                        concept=concept,
                                                                        name=form.cleaned_data['name'],
                                                                        defaults={'code': form.cleaned_data['code'],
                                                                                'description':form.cleaned_data['description'],
                                                                                'quality_status':form.cleaned_data['quality_status'],
                                                                                'created_by': self.request.user})
        return HttpResponseRedirect(self.get_success_url())
            
    def get_initial(self):
        initials = super().get_initial()
        initials['concept_id'] = self.kwargs.get('concept_id')
        return initials

    def get_success_url(self):
        if hasattr(self, 'return_url') and self.return_url:
            return self.return_url
        pk = self.kwargs.get('concept_id')
        return reverse('o_concept_detail', kwargs={'pk': pk})