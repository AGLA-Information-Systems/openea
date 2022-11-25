from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OSlot, OPredicate, OSlot


class OSlotDetailView(CustomPermissionRequiredMixin, DetailView):
    model = OSlot
    template_name = "o_slot/o_slot_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(OSlotDetailView, self).get_context_data(**kwargs)
        slot = context.get('object')
        model = slot.model
        concept = slot.concept
        
        predicates_as_subject = OPredicate.objects.filter(subject=concept).all()
        predicates_as_object = OPredicate.objects.filter(object=concept).all()
        context['inslots'] = {}
        context['ownslots'] = {}
        for x in predicates_as_subject:
            context['ownslots'][x.name] = list(OSlot.objects.filter(model=model, predicate=x, subject=slot).all())
        for x in predicates_as_object:
            context['inslots'][x.name] = list(OSlot.objects.filter(model=model, predicate=x, object=slot).all())
        
        context['model_id'] = model.id
        return context
