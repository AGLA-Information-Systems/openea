import re
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from ontology.models import OReport
from utils.views.custom import SingleObjectView

class OReportUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, UpdateView):
    model = OReport
    fields = ['name', 'description', 'path', 'content', 'model', 'quality_status',  'tags']
    template_name = "o_report/o_report_update.html"
    #success_url = reverse_lazy('o_report_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        path = form.cleaned_data['path']
        if path is not None:
            path = re.sub('/+','/', '/' + path.replace('.', '/'))
        form.instance.modified_by = self.request.user
        form.instance.modified_at = datetime.now()
        form.instance.path = path
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})