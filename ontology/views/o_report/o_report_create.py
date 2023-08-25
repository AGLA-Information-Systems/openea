import re
import traceback

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from utils.views.custom import CustomCreateView
from django.core.exceptions import SuspiciousOperation

from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.models import OReport
from openea.utils import Utils

class OReportCreateView(LoginRequiredMixin, CustomCreateView):
    model = OReport
    fields = ['name', 'description', 'path', 'content', 'model', 'quality_status',  'tags']
    template_name = "o_report/o_report_create.html"
    #success_url = reverse_lazy('o_report_list')
    permission_required = [(Utils.PERMISSION_ACTION_CREATE, model.get_object_type(), None)]

    def form_valid(self, form):
        try:
            path = form.cleaned_data['path']
            if path is not None:
                path = re.sub('/+','/', '/' + path.replace('.', '/'))
            form.instance, created = OReport.objects.get_or_create(
                name=form.cleaned_data['name'],
                model=form.cleaned_data['model'],
                organisation=form.cleaned_data['model'].organisation,
                defaults={
                    'path': path,
                    'content': form.cleaned_data['content'],
                    'description':form.cleaned_data['description'],
                    'quality_status':form.cleaned_data['quality_status'],
                    'created_by': self.request.user
                })
        except Exception as e:
            traceback.print_exc()
            raise SuspiciousOperation(str(e))
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('model_id')
        return reverse('o_model_detail', kwargs={'pk': pk})
