import json

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from ontology.controllers.o_model import ModelUtils
from ontology.models import OConcept, OInstance, OModel, OPredicate, ORelation
from openea.utils import Utils

from utils.views.custom import ReferrerView


class OModelCopyView(LoginRequiredMixin, ReferrerView, View):
    model = OModel
    targets = [OModel, OConcept, ORelation, OPredicate, OInstance]
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)] + \
                          [(Utils.PERMISSION_ACTION_VIEW, x.get_object_type(), None) for x in targets]

    def post(self, request, *args, **kwargs):
        
        model_id = kwargs.pop('model_id')
        model_1 = OModel.objects.get(id=model_id)
        
        self.get_current_organisation(request=request, args=args, kwargs=kwargs)
        
        new_model = ModelUtils.model_copy(model_1)
        
        return HttpResponseRedirect(reverse('o_model_detail', kwargs={'pk': new_model.id}))
    
    def get(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')
        self.object = OModel.objects.get(id=model_id)
        context = {"object": self.object}
        return render(request, "o_model/o_model_copy.html", context)
