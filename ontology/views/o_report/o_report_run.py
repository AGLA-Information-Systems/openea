from django.views import View
from django.views.generic.detail import SingleObjectMixin

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OReport
from utils.views.custom import SingleObjectView
from django.template.response import TemplateResponse

class OReportRunView(LoginRequiredMixin, SingleObjectView, SingleObjectMixin, View):
    model = OReport
    permission_required = [('EXECUTE', model.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = TemplateResponse(request, "reports" + self.object.path, context)
        return response
