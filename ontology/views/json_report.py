from django.shortcuts import render
from django.views.generic import View


from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.models import OModel
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class JSONReportView(LoginRequiredMixin, SingleObjectView, View):
    permission_required = [('EXPORT', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')

        return render(request, 'json_report.html', {'model_id': model_id})
