
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from authorization.controllers.utils import (
    CustomPermissionRequiredMixin, check_permission)
from authorization.models import Permission
from ontology.controllers.o_model import ModelUtils

from ontology.models import  OModel

from openea.utils import Utils

from utils.views.custom import ReferrerView


class OModelCopyView(LoginRequiredMixin, CustomPermissionRequiredMixin, ReferrerView, View):
    model = OModel
    permission_required = [(Permission.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        
        model_id = kwargs.pop('model_id')
        model_1 = OModel.objects.get(id=model_id)
        
        self.get_current_organisation(request=request, args=args, kwargs=kwargs)

        show_model = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_MODEL)
        show_relations = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_RELATION)
        show_concepts = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_CONCEPT)
        show_predicates = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_PREDICATE)
        show_instances = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_INSTANCE)

        if not (show_model and show_relations and show_concepts and show_predicates and show_instances):
            raise PermissionDenied('Permission Denied')
        
        new_model = ModelUtils.model_copy(model_1)
        
        return HttpResponseRedirect(reverse('o_model_detail', kwargs={'pk': new_model.id}))
    
    def get(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')
        self.object = OModel.objects.get(id=model_id)
        context = {"object": self.object}
        return render(request, "o_model/o_model_copy.html", context)