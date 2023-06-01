import base64
import json

from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from authorization.controllers.utils import (
    CustomPermissionRequiredMixin, check_permission,
    create_organisation_admin_security_group)
from authorization.models import Permission
from ontology.controllers.graphviz import GraphvizController
from ontology.controllers.o_model import ModelUtils
from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import OConcept, OInstance, OModel, OPredicate, OSlot
from ontology.plugins.json import GenericEncoder
from openea.utils import Utils


class OModelGapAnalysisView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = [('VIEW', OModel.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        model_1_id = ModelUtils.version_uuid(data.get('model_1_id'))
        model_1 = OModel.objects.get(id=model_1_id)
        model_2_id = ModelUtils.version_uuid(data.get('model_2_id'))
        model_2 = OModel.objects.get(id=model_2_id)
        filters = data.get('filters', [])

        show_model = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_MODEL)
        show_relations = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_RELATION)
        show_concepts = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_CONCEPT)
        show_predicates = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_PREDICATE)
        show_instances = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_INSTANCE)

        if not (show_model and show_relations and show_concepts and show_predicates and show_instances):
            raise PermissionDenied('Permission Denied')
        
        results = {
            'results': ModelUtils.model_diff(model_1=model_1, model_2=model_2, filters=filters),
            'model_1': ModelUtils.model_to_dict(model_1),
            'model_2': ModelUtils.model_to_dict(model_2)
        }
        
        return HttpResponse(json.dumps(results, cls=GenericEncoder), content_type="application/json")
    