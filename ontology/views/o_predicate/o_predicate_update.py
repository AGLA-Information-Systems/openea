from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_predicate.o_predicate_update import OPredicateUpdateForm
from django.utils import timezone
from ontology.models import OPredicate
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class OPredicateUpdateView(LoginRequiredMixin, SingleObjectView, UpdateView):
    model = OPredicate
    template_name = "o_predicate/o_predicate_update.html"
    form_class = OPredicateUpdateForm
    #success_url = reverse_lazy('o_predicate_list')
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