from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.forms.o_slot.o_slot_create import OSlotCreateForm
from django.views.generic.edit import FormView

from ontology.models import OConcept, OInstance, OPredicate, OSlot, OModel
from utils.generic import handle_errors
from utils.views.custom import ReferrerView

class OSlotCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, ReferrerView, FormView):
    model = OSlot
    template_name = "o_slot/o_slot_create.html"
    form_class = OSlotCreateForm
    #success_url = reverse_lazy('o_slot_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    @handle_errors
    def form_valid(self, form):
        self.return_url = self.request.POST.get('return_url')
        form.instance.created_by = self.request.user
        is_subject = self.kwargs.get('is_subject') == '1'
        concept = OConcept.objects.get(id=self.kwargs.get('concept_id'))
        instance = OInstance.objects.get(id=self.kwargs.get('instance_id'))
        predicate = OPredicate.objects.get(id=self.kwargs.get('predicate_id'))
        model = instance.model

        new_instance = None
        new_instance_name = form.cleaned_data['new_object_name']
        new_instance_desc = form.cleaned_data['new_object_description']
        
        subject = form.cleaned_data['subject']
        object = form.cleaned_data['object']
        order = form.cleaned_data['order']

        if object is None or subject is None:
            if is_subject:
                possible_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=predicate.object)] + [predicate.object]
            else:
                possible_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=predicate.subject)] + [predicate.subject]
            
            if not new_instance_name:
                raise ValueError('NO_INSTANCE_NAME')
            
            if concept in possible_concepts:
                new_instance_concept = concept
                new_instance, created = OInstance.objects.get_or_create(
                    model=model, 
                    concept=new_instance_concept,
                    name=new_instance_name,
                    defaults={'description': new_instance_desc})
            if is_subject:
                object = new_instance
            else:
                subject = new_instance
        
        slots_count = OSlot.objects.filter(model=model, predicate=predicate, subject=subject).count()
        if predicate.cardinality_max != 0 and slots_count >= predicate.cardinality_max:
            raise ValueError('MAX_SLOTS_REACHED')

        slot, created = OSlot.objects.get_or_create(
            model=model, 
            predicate=predicate, 
            subject=subject,
            object=object,
            order=order
        )
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['is_subject'] =  self.kwargs.get('is_subject') == '1'
        initials['instance_id'] =  self.kwargs.get('instance_id')
        initials['predicate_id'] = self.kwargs.get('predicate_id')
        return initials

    def get_success_url(self):
        if self.return_url:
            return self.return_url
        pk = self.kwargs.get('instance_id')
        return reverse('o_instance_detail', kwargs={'pk': pk})
