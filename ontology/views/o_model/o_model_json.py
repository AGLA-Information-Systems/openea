import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import View

from openea.utils import Utils
from ontology.controllers.o_model import ModelUtils
from ontology.models import OModel
from ontology.plugins.json import GenericEncoder


class OModelJSONFilterView(LoginRequiredMixin, View):
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, OModel.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        filtered_data = ModelUtils.filter(user=self.request.user, data=data)
        
        result = {
            'relations': [ModelUtils.relation_to_dict(x) for x in filtered_data['relations']],
            'concepts': [ModelUtils.concept_to_dict(x) for x in filtered_data['concepts']],
            'predicates': [ModelUtils.predicate_to_dict(x) for x in filtered_data['predicates']],
            'instances': [ModelUtils.instance_to_dict(x) for x in filtered_data['instances']],
            'slots': [ModelUtils.slot_to_dict(x) for x in filtered_data['slots']]
        }

        return HttpResponse(json.dumps(result, cls=GenericEncoder), content_type="application/json")
    