from django.http import Http404
from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OReport
from utils.views.custom import SingleObjectView


class OReportDetailView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = OReport
    template_name = "o_report/o_report_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
   
    def get_context_data(self, **kwargs):
        context = super(OReportDetailView, self).get_context_data(**kwargs)
        report = context.get('object')
        model=report.model
        context['model_id'] = model.id
        return context
