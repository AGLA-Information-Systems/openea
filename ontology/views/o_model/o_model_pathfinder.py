import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from django.views.generic import View
from ontology.controllers.o_model import ModelUtils

from ontology.models import OConcept, OInstance, OModel, OPredicate, ORelation
from ontology.plugins.json import GenericEncoder
from openea.utils import Utils


class OModelPathFinderView(LoginRequiredMixin, View):
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, OModel.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        start_instance_id = ModelUtils.version_uuid(data.get('start_instance_id'))
        start_instance = OInstance.objects.get(id=start_instance_id)
        end_instance_id = ModelUtils.version_uuid(data.get('end_instance_id'))
        end_instance = OInstance.objects.get(id=end_instance_id)
        
        show_relations = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, ORelation.get_object_type(), None))
        show_concepts = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OConcept.get_object_type(), None))
        show_predicates = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OPredicate.get_object_type(), None))
        show_instances = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, OInstance.get_object_type(), None))

        if not (show_relations and show_concepts and show_predicates and show_instances):
            raise PermissionDenied('Permission Denied')
        
        result = ModelUtils.find_paths(start_instance=start_instance, end_instance=end_instance)

        return HttpResponse(json.dumps(result, cls=GenericEncoder), content_type="application/json")
    