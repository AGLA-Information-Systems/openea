from django.http import Http404
from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OSlot, OPredicate, OSlot
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class OSlotDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = OSlot
    template_name = "o_slot/o_slot_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(OSlotDetailView, self).get_context_data(**kwargs)
        slot = context.get('object')
        model = slot.model
        
        context['model_id'] = model.id
        return context
