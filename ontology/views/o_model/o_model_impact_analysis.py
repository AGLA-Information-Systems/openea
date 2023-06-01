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
from ontology.controllers.graphviz import GraphizController
from ontology.controllers.o_model import ModelUtils
from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import OConcept, OInstance, OModel, OPredicate, OSlot
from ontology.plugins.json import GenericEncoder
from openea.utils import Utils


class OModelImpactAnalysisView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = [('VIEW', OModel.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        model_id = kwargs.pop('model_id')
        model = OModel.objects.get(id=model_id)

        root_instance_id = ModelUtils.version_uuid(data.get('root_instance_id'))
        root_instance = OInstance.objects.get(id=root_instance_id)
        predicate_ids = data.get('predicate_ids', [])
        if isinstance(predicate_ids, str):
            predicate_ids = [predicate_ids]
        level = int(data.get('level', 10)) + 1
        
        show_relations = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_RELATION)
        show_concepts = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_CONCEPT)
        show_predicates = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_PREDICATE)
        show_instances = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_INSTANCE)

        if not (show_relations and show_concepts and show_predicates and show_instances):
            raise PermissionDenied('Permission Denied')
        
        results = ModelUtils.analyze_impact(root_instance=root_instance, predicate_ids=predicate_ids, level=level)
        dictified_results = ModelUtils.dictify_impact_analysis(results)
        
        graph_data = {
            'model': model,
            'nodes': results
        }
        svg_str = GraphizController.render_impact_analysis(format='svg', data=graph_data)
        xmlSoup = BeautifulSoup(svg_str, 'html.parser')
        graph = xmlSoup.find('svg')

        result = {
            'data': dictified_results,
            'graph': base64.b64encode(graph.encode('ascii')).decode("utf-8")
        }

        return HttpResponse(json.dumps(result, cls=GenericEncoder), content_type="application/json")
    