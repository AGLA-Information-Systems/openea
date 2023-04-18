from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_concept.o_concept_create import OConceptCreateForm
from ontology.models import OConcept

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"

class OConceptCreateView(CustomPermissionRequiredMixin, CreateView):
    model = OConcept
    form_class = OConceptCreateForm
    template_name = "o_concept/o_concept_create.html"
    #success_url = reverse_lazy('o_concept_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance, created = OConcept.objects.get_or_create(model=form.cleaned_data['model'],
                                                                    name=form.cleaned_data['name'],
                                                                    defaults={'description':form.cleaned_data['description'],
                                                                              'quality_status':form.cleaned_data['quality_status'],
                                                                              'created_by': self.request.user})
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initials = super().get_initial()
        initials['model_id'] = self.kwargs.get('model_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('model_id')
        return reverse('o_model_detail', kwargs={'pk': pk})
