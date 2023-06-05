from django.http import HttpResponse
import json

from django.views.generic import View
from authorization.controllers.utils import CustomPermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.controllers.o_model import ModelUtils

from ontology.models import OModel
from ontology.plugins.json import GenericEncoder


class OModelJSONView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = [('VIEW', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')
        model = OModel.objects.get(id=model_id)
        model_dict = ModelUtils.instances_to_dict(model=model)
        return HttpResponse(json.dumps(model_dict, cls=GenericEncoder), content_type="application/json")


class OModelJSONFilterView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = [('VIEW', OModel.get_object_type(), None)]

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
    