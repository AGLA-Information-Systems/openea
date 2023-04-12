from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OReport
from utils.views.custom import SingleObjectView


class OReportRunView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = OReport
    template_name = "o_report/o_report_run.html"
    permission_required = [('RUN', model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(OReportRunView, self).get_context_data(**kwargs)
        report = context.get('object')
        model=report.model
        context['report_path'] = 'reports/' + report.path
        context['model_id'] = model.id
        return context
