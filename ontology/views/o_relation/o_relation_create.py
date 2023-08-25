import traceback
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from utils.views.custom import CustomCreateView
from django.core.exceptions import SuspiciousOperation

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_relation.o_relation_create import ORelationCreateForm
from ontology.models import ORelation
from openea.utils import Utils

class ORelationCreateView(LoginRequiredMixin, CustomCreateView):
    model = ORelation
    form_class = ORelationCreateForm
    template_name = "o_relation/o_relation_create.html"
    #success_url = reverse_lazy('o_relation_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def form_valid(self, form):
        try:
            form.instance, created = ORelation.objects.get_or_create(
                name=form.cleaned_data['name'],
                type=form.cleaned_data['type'],
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