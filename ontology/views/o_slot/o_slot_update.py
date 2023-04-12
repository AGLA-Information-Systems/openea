from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.controllers.knowledge_base import KnowledgeBaseController
from ontology.forms.o_slot.o_slot_update import OSlotUpdateForm
from django.views.generic.edit import FormView

from ontology.models import OInstance, OSlot, OPredicate, OSlot
from utils.views.custom import SingleObjectView

class OSlotUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, FormView):
    model = OSlot
    template_name = "o_slot/o_slot_update.html"
    form_class = OSlotUpdateForm
    #success_url = reverse_lazy('o_slot_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        self.return_url = self.request.POST.get('return_url')
        form.instance.created_by = self.request.user
        slot = OSlot.objects.get(id=self.kwargs.get('pk'))
        self.object = slot
        #TODO: handle subject and object
        object=OInstance.objects.get(id=form.cleaned_data['object'].id)
        slot.object=object
        slot.order=form.cleaned_data['order']
        slot.save()
            
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['slot_id'] = self.kwargs.get('pk')
        return initials

    def get_success_url(self):
        if self.return_url:
            return self.return_url
        pk = self.object.id
        return reverse('o_slot_detail', kwargs={'pk': pk})