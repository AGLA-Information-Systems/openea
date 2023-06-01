import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from authorization.controllers.utils import (
    CustomPermissionRequiredMixin, check_permission,
    create_organisation_admin_security_group)
from authorization.models import Permission
from ontology.controllers.o_model import ModelUtils
from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import OConcept, OInstance, OModel, OPredicate, OSlot
from ontology.plugins.json import GenericEncoder
from openea.utils import Utils


class OModelPathFinderView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = [('VIEW', OModel.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        start_instance_id = ModelUtils.version_uuid(data.get('start_instance_id'))
        start_instance = OInstance.objects.get(id=start_instance_id)
        end_instance_id = ModelUtils.version_uuid(data.get('end_instance_id'))
        end_instance = OInstance.objects.get(id=end_instance_id)
        
        show_relations = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_RELATION)
        show_concepts = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_CONCEPT)
        show_predicates = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_PREDICATE)
        show_instances = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_INSTANCE)

        if not (show_relations and show_concepts and show_predicates and show_instances):
            raise PermissionDenied('Permission Denied')
        
        result = ModelUtils.find_paths(start_instance=start_instance, end_instance=end_instance)

        return HttpResponse(json.dumps(result, cls=GenericEncoder), content_type="application/json")
    