import re

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.models import OReport


class OReportCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, CreateView):
    model = OReport
    fields = ['name', 'description', 'path', 'content', 'model', 'quality_status',  'tags']
    template_name = "o_report/o_report_create.html"
    #success_url = reverse_lazy('o_report_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            path = form.cleaned_data['path']
            if path is not None:
                path = re.sub('/+','/', '/' + path.replace('.', '/'))
            form.instance, created = OReport.objects.get_or_create(model=form.cleaned_data['model'],
                                                                name=form.cleaned_data['name'],
                                                                defaults={'path': path,
                                                                            'content': form.cleaned_data['content'],
                                                                            'description':form.cleaned_data['description'],
                                                                            'quality_status':form.cleaned_data['quality_status'],
                                                                            'created_by': self.request.user})
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('model_id')
        return reverse('o_model_detail', kwargs={'pk': pk})
