import re
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OReport

class OReportCreateView(CustomPermissionRequiredMixin, CreateView):
    model = OReport
    fields = ['name', 'description', 'path', 'content', 'model', 'quality_status',  'tags']
    template_name = "o_report/o_report_create.html"
    #success_url = reverse_lazy('o_report_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance = OReport.get_or_create(model=form.cleaned_data['model'], name=form.cleaned_data['name'], path=form.cleaned_data['path'], content=form.cleaned_data['content'], description=form.cleaned_data['description'])
            form.instance.created_by = self.request.user
            if form.instance.path is not None:
                form.instance.path = re.sub('/+','/', '/' + form.instance.path.replace('..', '/'))
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('model_id')
        return reverse('o_model_detail', kwargs={'pk': pk})