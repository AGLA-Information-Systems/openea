from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OReport

class OReportListView(CustomPermissionRequiredMixin, ListView):
    model = OReport
    template_name = "o_report/o_report_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]
