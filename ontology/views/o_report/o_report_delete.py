from django.http import Http404
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from ontology.models import OReport
from utils.views.custom import SingleObjectView

class OReportDeleteView(CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = OReport
    template_name = "o_report/o_report_delete.html"
    #success_url = reverse_lazy('o_report_list')
    permission_required = [('DELETE', model.get_object_type(), None)]
  
    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})
