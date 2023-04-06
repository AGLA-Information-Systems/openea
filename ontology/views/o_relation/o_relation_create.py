from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.forms.o_relation.o_relation_create import ORelationCreateForm
from ontology.models import ORelation


class ORelationCreateView(CustomPermissionRequiredMixin, CreateView):
    model = ORelation
    form_class = ORelationCreateForm
    template_name = "o_relation/o_relation_create.html"
    #success_url = reverse_lazy('o_relation_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance, created = ORelation.objects.get_or_create(model=form.cleaned_data['model'],
                                                                    name=form.cleaned_data['name'],
                                                                    type=form.cleaned_data['type'],
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