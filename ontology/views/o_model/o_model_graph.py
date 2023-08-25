import json
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.views import View


from openea.utils import Utils
from ontology.controllers.graphviz import GraphvizController
from ontology.controllers.o_model import ModelUtils
from ontology.models import OModel
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class OModelGraphView(LoginRequiredMixin, SingleObjectView, View):
    model = OModel
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def post(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')
        model = OModel.objects.get(id=model_id)

        data=json.loads(request.body)
        knowledge_set = data.get('knowledge_set', 'instances')
        data = ModelUtils.filter(user=self.request.user, data=data)
        data['model'] = model

        svg_str = GraphvizController.render_model_graph(format='svg', model_data=data, knowledge_set=knowledge_set)

        xmlSoup = BeautifulSoup(svg_str, 'html.parser')
        image = xmlSoup.find('svg')
        return HttpResponse(str(image), content_type="text/html")
