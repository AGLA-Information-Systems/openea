import io
import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View


from ontology.controllers.o_model import ModelUtils
from ontology.forms import ModelExportForm, ModelImportForm
from ontology.models import OModel
from ontology.plugins.json import GenericEncoder
from organisation.constants import TIME_SCHEDULE_NOW, TIME_SCHEDULE_SCHEDULED
from organisation.controllers.filestore import MediaFileStorage
from organisation.controllers.tasks import TaskController
from organisation.models import TASK_STATUS_SUCCESS, TASK_TYPE_IMPORT, Task


class ModelImportView(LoginRequiredMixin, View):
    form_class = ModelImportForm
    template_name = 'o_model/o_model_import.html'
    success_url = reverse_lazy('task_list')
    initial = {}
    permission_required = [('IMPORT', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        self.initial['model'] = self.kwargs.get('model_id')
        model = OModel.objects.get(id=self.initial['model'])
        form = self.form_class(initial=self.initial, user=self.request.user)
        return render(request, self.template_name, {'form': form, 'ontology_data': json.dumps(ModelUtils.ontology_to_dict(model=model), cls=GenericEncoder)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, user=self.request.user)
        model_id = kwargs.pop('model_id')
        model = OModel.objects.get(id=model_id)

        if form.is_valid():
            # <process form cleaned data>
            media_storage = MediaFileStorage
            model = form.cleaned_data.get('model')
            organisation = model.repository.organisation

            import_file = media_storage.store_file(organisation=organisation, uploaded_file=request.FILES['import_file'])
            config = {
                'model_id': str(model.id),
                'format': form.cleaned_data.get('format'),
                'knowledge_set': form.cleaned_data.get('knowledge_set'),
                'time_schedule': form.cleaned_data.get('time_schedule', TIME_SCHEDULE_SCHEDULED),

                'concepts': request.POST.get('concepts'),
                'relations': request.POST.get('relations'),
                'predicates': request.POST.get('predicates'),
                'instances': request.POST.get('instances')
            }

            t = Task.objects.create(
                name='import',
                description='',
                type=TASK_TYPE_IMPORT,
                attachment=import_file,
                config=json.dumps(config),
                user=self.request.user,
                organisation=organisation,
                created_by=self.request.user)
            t.save()
            
            if config.get("time_schedule") == TIME_SCHEDULE_NOW:
                
                TaskController.process_task(t)
                if t.status == TASK_STATUS_SUCCESS:
                    return HttpResponseRedirect(reverse('task_detail', kwargs={'pk': t.id}))
                else:
                    raise SuspiciousOperation('Unable to process the task %s: %s' %(str(t.id), str(t.error)))
                
            elif config.get("time_schedule") == TIME_SCHEDULE_SCHEDULED:
                return HttpResponseRedirect(reverse('task_detail', kwargs={'pk': t.id}))
            else:
                raise SuspiciousOperation('Unknown time_schedule: '+ config.get("time_schedule"))

        return render(request, self.template_name, {'form': form, 'ontology_data': json.dumps(ModelUtils.ontology_to_dict(model=model), cls=GenericEncoder)})

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})
