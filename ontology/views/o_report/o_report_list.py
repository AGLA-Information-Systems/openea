from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OReport
from openea.utils import Utils
from utils.views.custom import MultipleObjectsView

class OReportListView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = OReport
    template_name = "o_report/o_report_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.is_staff:
            return qs
        if self.request.user.active_profile is not None:
            ids= [x.id for x in qs.all() if x.organisation == self.request.user.active_profile.organisation]
            return qs.filter(id__in=ids)
        return qs.none()