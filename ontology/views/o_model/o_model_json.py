from django.http import HttpResponse
import json
from django.shortcuts import render
from django.views.generic import View
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.controllers.utils import KnowledgeBaseUtils

from ontology.models import OConcept, OInstance, OModel, OPredicate, OSlot
from ontology.plugins.json import GenericEncoder


class OModelJSONView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = [('VIEW', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')
        model = OModel.objects.get(id=model_id)
        model_dict = KnowledgeBaseUtils.instances_to_dict(model=model)
        return HttpResponse(json.dumps(model_dict, cls=GenericEncoder), content_type="application/json")

