from django.http import Http404
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from ontology.models import OPredicate
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class OPredicateDeleteView(LoginRequiredMixin, SingleObjectView, DeleteView):
    model = OPredicate
    template_name = "o_predicate/o_predicate_delete.html"
    #success_url = reverse_lazy('o_predicate_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})