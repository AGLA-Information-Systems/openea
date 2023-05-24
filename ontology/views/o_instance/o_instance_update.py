from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView

from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.forms.o_instance.o_instance_update import OInstanceUpdateForm
from ontology.models import OInstance, OPredicate, OSlot
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class OInstanceUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, FormView):
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
            instance.concept = form.cleaned_data.get('concept', '')
            instance.description = form.cleaned_data.get('description', '')
            instance.quality_status = form.cleaned_data.get('quality_status', '')
            #instance.tag_groups = form.cleaned_data.get('tag_groups')
            instance.tags.set(form.cleaned_data.get('tags', []))

            instance.save()

            predicates_as_subject = OPredicate.objects.filter(subject=concept).all()
            predicates_as_object = OPredicate.objects.filter(object=concept).all()

            # for x in predicates_as_subject:
            #     object_concept = x.object
            #     if object_concept.name == Utils.RESOURCE_CONCEPT:
            #         slot_value = form.cleaned_data.get(x.name, '')
            #         slot = OSlot.get_or_create(model=model, predicate=x, subject=instance, value=slot_value)
            #     else:
            #         slot_values = form.cleaned_data.get(x.name, [])
            #         for slot_value in slot_values:
            #             slot = OSlot.get_or_create(model=model, predicate=x, subject=instance, value=slot_value)
                    
            # for x in predicates_as_object:
            #     subject_concept = x.subject
            #     if subject_concept.name == Utils.RESOURCE_CONCEPT:
            #         slot_value = form.cleaned_data.get(x.name, '')
            #         slot = OSlot.get_or_create(model=model, predicate=x, subject=slot_value, object=instance)
            #     else:
            #         slot_values = form.cleaned_data.get(x.name, [])
            #         for slot_value in slot_values:
            #             slot = OSlot.get_or_create(model=model, predicate=x, subject=slot_value, object=instance)

            for x in predicates_as_subject:
                object_concept = x.object
                slot_values = form.cleaned_data.get(x.name, [])
                for slot_value in slot_values:
                    slot, created = OSlot.objects.get_or_create(model=model, predicate=x, subject=instance, object=slot_value)

        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initials = super().get_initial()
        initials['pk'] = self.kwargs.get('pk')
        return initials

    def get_success_url(self):
        return reverse('o_instance_detail', kwargs={'pk': self.kwargs.get('pk')})
