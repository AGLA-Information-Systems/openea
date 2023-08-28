import traceback
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from ontology.controllers.o_model import ModelUtils
from utils.views.custom import CustomCreateView
from django.core.exceptions import SuspiciousOperation

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_model.o_model_create import OModelCreateForm
from ontology.models import OModel
from openea.utils import Utils

class OModelCreateView(LoginRequiredMixin, CustomCreateView):
    model = OModel
    template_name = "o_model/o_model_create.html"
    form_class = OModelCreateForm
    #success_url = reverse_lazy('o_model_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def get_initial(self):
        initials = super().get_initial()
        initials['repository'] = self.kwargs.get('repository_id')
        return initials

    def form_valid(self, form):
        try:
            form.instance, created = OModel.objects.get_or_create(
                name=form.cleaned_data['name'],
                version=form.cleaned_data['version'] or '1.0', 
                repository=form.cleaned_data['repository'],
                organisation=form.cleaned_data['repository'].organisation,
                defaults={
                    'description': form.cleaned_data['description'],
                    'created_by': self.request.user
                })
            
            root_concept = None
            if form.cleaned_data['root_concept_name']:
                root_concept = ModelUtils.set_root_concept(model=form.instance, root_concept_name=form.cleaned_data['root_concept_name'])

            if form.cleaned_data['native_concepts'] is True:
                ModelUtils.add_native_concepts(model=form.instance, root_concept=root_concept)

        except Exception as e:
            traceback.print_exc()
            raise SuspiciousOperation(str(e))
        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        pk = self.kwargs['repository_id']
        return reverse('repository_detail', kwargs={'pk': pk})
