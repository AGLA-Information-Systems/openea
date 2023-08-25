from django.http import JsonResponse
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OInstance, OSlot
from openea.utils import Utils

class OInstanceJSONListView(LoginRequiredMixin, View):
    model = OInstance
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        model_id = request.GET.get('model_id', '')
        concept_id = request.GET.get('concept_id', '')

        if model_id:
            instances = OInstance.objects.filter(model_id=model_id)
        elif concept_id:
            instances = OInstance.objects.filter(concept_id=concept_id)
        else:
            instances = OInstance.objects.all()
            
        data = {}
        for instance in instances:
            data[str(instance.id)] = {
                "id": instance.id,
                "name": instance.name,
                "concept": instance.concept.name,
                "ownslots": {},
            }
            for slot in OSlot.objects.filter(model=instance.model, subject=instance).all():
                data[str(instance.id)]["ownslots"][str(slot.id)] = {
                    "id": slot.id,
                    "relation": slot.predicate.relation.name,
                    "object_id": slot.object.id if slot.object is not None else None,
                }
        return JsonResponse(data, safe=False)