import traceback
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from utils.views.custom import CustomCreateView
from django.core.exceptions import SuspiciousOperation

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_concept.o_concept_create import OConceptCreateForm
from ontology.models import OConcept
from openea.utils import Utils


class OConceptCreateView(LoginRequiredMixin, CustomCreateView):
    model = OConcept
    form_class = OConceptCreateForm
    template_name = "o_concept/o_concept_create.html"
    #success_url = reverse_lazy('o_concept_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def form_valid(self, form):
        try:
            form.instance, created = OConcept.objects.get_or_create(
                name=form.cleaned_data['name'],
                model=form.cleaned_data['model'],
                organisation=form.cleaned_data['model'].organisation,
                defaults={
                    'description':form.cleaned_data['description'],
                    'quality_status':form.cleaned_data['quality_status'],
                    'created_by': self.request.user
                })
        except Exception as e:
            traceback.print_exc()
            raise SuspiciousOperation(str(e))
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initials = super().get_initial()
        initials['model_id'] = self.kwargs.get('model_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('model_id')
        return reverse('o_model_detail', kwargs={'pk': pk})
