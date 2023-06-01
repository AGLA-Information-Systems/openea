import json
from django.views import View                               
from authorization.models import Permission
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from authorization.controllers.utils import check_permission
from ontology.controllers.graphviz import GraphizController

from django.http import Http404, HttpResponse, HttpResponseBadRequest
from ontology.controllers.o_model import ModelUtils

from utils.views.custom import SingleObjectView
from openea.utils import Utils
from xml.etree import ElementTree as ET
from ontology.models import OInstance, OModel
from bs4 import BeautifulSoup

class OModelGraphView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, View):
    model = OModel
    permission_required = [(Permission.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')
        model = OModel.objects.get(id=model_id)

        data=json.loads(request.body)
        knowledge_set = data.get('knowledge_set', 'instances')
        data = ModelUtils.filter(user=self.request.user, data=data)
        data['model'] = model

        svg_str = GraphizController.build(format='svg', model_data=data, knowledge_set=knowledge_set)

        xmlSoup = BeautifulSoup(svg_str, 'html.parser')
        image = xmlSoup.find('svg')
        return HttpResponse(str(image), content_type="text/html")
