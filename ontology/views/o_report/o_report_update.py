import re
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OReport

class OReportUpdateView(CustomPermissionRequiredMixin, UpdateView):
    model = OReport
    fields = ['name', 'description', 'path', 'content', 'model', 'quality_status',  'tags']
    template_name = "o_report/o_report_update.html"
    #success_url = reverse_lazy('o_report_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
            form.instance.path = re.sub('/+','/', '/' + form.instance.path)
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})