from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.forms.o_instance.o_instance_update import OInstanceUpdateForm
from django.views.generic.edit import FormView

from ontology.models import OInstance, OPredicate, OSlot

class OInstanceUpdateView(CustomPermissionRequiredMixin, FormView):
    model = OInstance
    template_name = "o_instance/o_instance_update.html"
    form_class = OInstanceUpdateForm
    #success_url = reverse_lazy('o_instance_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
            instance = OInstance.objects.get(id=self.kwargs.get('pk'))
            self.object = instance
            model = instance.model
            concept = instance.concept

            instance.name = form.cleaned_data.get('name', None)
            instance.code = form.cleaned_data.get('code', None)
            instance.description = form.cleaned_data.get('description', '')
            #instance.tag_groups = form.cleaned_data.get('tag_groups')
            instance.tags.set(form.cleaned_data.get('tags', []))

            instance.save()

            predicates_as_subject = OPredicate.objects.filter(subject=concept).all()
            predicates_as_object = OPredicate.objects.filter(object=concept).all()

            for x in predicates_as_subject:
                slot_values = form.cleaned_data.get(x.name, [])
                for slot_value in slot_values:
                    slot = OSlot.objects.get_or_create(model=model, predicate=x, subject=instance, object=slot_value)
                    
            for x in predicates_as_object:
                slot_values = form.cleaned_data.get(x.name, [])
                for slot_value in slot_values:
                    slot = OSlot.objects.get_or_create(model=model, predicate=x, subject=slot_value, object=instance)

        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['pk'] = self.kwargs.get('pk')
        return initials

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})