from django.shortcuts import render
from django.views.generic import View

from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.models import OModel
from utils.views.custom import SingleObjectView


class JSONReportView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, View):
    permission_required = [('EXPORT', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')

        return render(request, 'json_report.html', {'model_id': model_id})
