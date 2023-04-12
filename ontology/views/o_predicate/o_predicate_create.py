from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_predicate.o_predicate_create import OPredicateCreateForm
from ontology.models import OPredicate


class OPredicateCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, CreateView):
    model = OPredicate
    template_name = "o_predicate/o_predicate_create.html"
    form_class = OPredicateCreateForm
    #success_url = reverse_lazy('o_predicate_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance, created = OPredicate.objects.get_or_create(model=form.cleaned_data['model'],
                                                                    subject=form.cleaned_data['subject'], 
                                                                    relation=form.cleaned_data['relation'],
                                                                    object=form.cleaned_data['object'],
                                                                    defaults={'cardinality_min': form.cleaned_data['cardinality_min'],
                                                                            'cardinality_max': form.cleaned_data['cardinality_max'],
                                                                            'description': form.cleaned_data['description'],
                                                                            'quality_status':form.cleaned_data['quality_status'],
                                                                            'created_by': self.request.user})
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        #form = OPredicateCreateForm(model_id=initials['model'])
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('model_id')
        return reverse('o_model_detail', kwargs={'pk': pk})
