from django.http import Http404
from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OReport
from openea.utils import Utils
from utils.views.custom import SingleObjectView


class OReportDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = OReport
    template_name = "o_report/o_report_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
   
    def get_context_data(self, **kwargs):
        context = super(OReportDetailView, self).get_context_data(**kwargs)
        report = context.get('object')
        model=report.model
        context['model_id'] = model.id
        return context
