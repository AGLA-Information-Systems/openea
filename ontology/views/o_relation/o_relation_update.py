from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_relation.o_relation_update import ORelationUpdateForm
from django.utils import timezone
from ontology.models import ORelation
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class ORelationUpdateView(LoginRequiredMixin, SingleObjectView, UpdateView):
    model = ORelation
    form_class = ORelationUpdateForm
    template_name = "o_relation/o_relation_update.html"
    form_class = ORelationUpdateForm
    #success_url = reverse_lazy('o_relation_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_at = timezone.now()
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['pk'] = self.kwargs.get('pk')
        return initials

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})