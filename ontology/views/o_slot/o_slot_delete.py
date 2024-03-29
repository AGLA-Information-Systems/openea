from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from ontology.models import OConcept, OSlot
from openea.utils import Utils
from utils.views.custom import SingleObjectView

class OSlotDeleteView(LoginRequiredMixin, SingleObjectView, DeleteView):
    model = OSlot
    template_name = "o_slot/o_slot_delete.html"
    #success_url = reverse_lazy('o_slot_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    def get_initial(self):
        initials = super().get_initial()
        initials['slot_id'] = self.kwargs.get('pk')
        return initials
    
    def form_valid(self, request, *args, **kwargs):
        self.return_url = self.request.POST.get('return_url')
        return super(OSlotDeleteView, self).form_valid(request, *args, **kwargs)
    
    def get_success_url(self):
        if hasattr(self, 'return_url') and self.return_url:
            return self.return_url
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})
