
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from ontology.controllers.o_model import ModelUtils

from ontology.models import OConcept, OInstance, OModel, OPredicate, ORelation
from ontology.plugins.json import GenericEncoder
from openea.utils import Utils


class OModelGapAnalysisView(LoginRequiredMixin, View):
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, OModel.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        model_1_id = ModelUtils.version_uuid(data.get('model_1_id'))
        model_1 = OModel.objects.get(id=model_1_id)
        model_2_id = ModelUtils.version_uuid(data.get('model_2_id'))
        model_2 = OModel.objects.get(id=model_2_id)
        filters = data.get('filters', [])

        show_model = self.request.user.acl.check(organisation=model_1.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OModel.get_object_type(), None)) \
                     and self.request.user.acl.check(organisation=model_2.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OModel.get_object_type(), None))
        show_relations = self.request.user.acl.check(organisation=model_1.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, ORelation.get_object_type(), None)) \
                         and self.request.user.acl.check(organisation=model_2.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, ORelation.get_object_type(), None))
        show_concepts = self.request.user.acl.check(organisation=model_1.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OConcept.get_object_type(), None)) \
                        and self.request.user.acl.check(organisation=model_2.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OConcept.get_object_type(), None))
        show_predicates = self.request.user.acl.check(organisation=model_1.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OPredicate.get_object_type(), None)) \
                         and self.request.user.acl.check(organisation=model_2.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OPredicate.get_object_type(), None))
        show_instances = self.request.user.acl.check(organisation=model_1.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OInstance.get_object_type(), None)) \
                        and self.request.user.acl.check(organisation=model_2.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OInstance.get_object_type(), None))

        if not (show_model and show_relations and show_concepts and show_predicates and show_instances):
            raise PermissionDenied('Permission Denied')
        
        results = {
            'results': ModelUtils.model_diff(model_1=model_1, model_2=model_2, filters=filters),
            'model_1': ModelUtils.model_to_dict(model_1),
            'model_2': ModelUtils.model_to_dict(model_2)
        }
        
        return HttpResponse(json.dumps(results, cls=GenericEncoder), content_type="application/json")
    