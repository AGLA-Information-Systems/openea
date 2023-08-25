import traceback
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from utils.views.custom import CustomCreateView
from django.core.exceptions import SuspiciousOperation

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_predicate.o_predicate_create import OPredicateCreateForm
from ontology.models import OPredicate
from openea.utils import Utils

class OPredicateCreateView(LoginRequiredMixin, CustomCreateView):
    model = OPredicate
    template_name = "o_predicate/o_predicate_create.html"
    form_class = OPredicateCreateForm
    #success_url = reverse_lazy('o_predicate_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def form_valid(self, form):
        try:
            form.instance, created = OPredicate.objects.get_or_create(
                subject=form.cleaned_data['subject'], 
                relation=form.cleaned_data['relation'],
                object=form.cleaned_data['object'],
                model=form.cleaned_data['model'],
                organisation=form.cleaned_data['model'].organisation,
                defaults={
                    'cardinality_min': form.cleaned_data['cardinality_min'],
                    'cardinality_max': form.cleaned_data['cardinality_max'],
                    'description': form.cleaned_data['description'],
                    'quality_status':form.cleaned_data['quality_status'],
                    'created_by': self.request.user
                })
        except Exception as e:
            traceback.print_exc()
            raise SuspiciousOperation(str(e))
        
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        #form = OPredicateCreateForm(model_id=initials['model'])
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('model_id')
        return reverse('o_model_detail', kwargs={'pk': pk})
