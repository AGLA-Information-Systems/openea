import base64
import json

from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from ontology.controllers.graphviz import GraphvizController
from ontology.controllers.o_model import ModelUtils
from ontology.models import  OConcept, OInstance, OModel, OPredicate, ORelation
from ontology.plugins.json import GenericEncoder
from openea.utils import Utils


class OModelImpactAnalysisView(LoginRequiredMixin, View):
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, OModel.get_object_type(), None)]

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
        
        show_relations = self.request.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, ORelation.get_object_type(), None))
        show_concepts = self.request.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OConcept.get_object_type(), None))
        show_predicates = self.request.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OPredicate.get_object_type(), None))
        show_instances = self.request.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OInstance.get_object_type(), None))

        if not (show_relations and show_concepts and show_predicates and show_instances):
            raise PermissionDenied('Permission Denied')
        
        results = ModelUtils.analyze_impact(root_instance=root_instance, predicate_ids=predicate_ids, level=level)
        dictified_results = ModelUtils.dictify_impact_analysis(results)
        
        graph_data = {
            'model': model,
            'nodes': results
        }
        svg_str = GraphvizController.render_impact_analysis(format='svg', data=graph_data)
        xmlSoup = BeautifulSoup(svg_str, 'html.parser')
        graph = xmlSoup.find('svg')

        result = {
            'data': dictified_results,
            'graph': base64.b64encode(graph.encode('ascii')).decode("utf-8")
        }

        return HttpResponse(json.dumps(result, cls=GenericEncoder), content_type="application/json")
    