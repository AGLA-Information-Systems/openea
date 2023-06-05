import io
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (FileResponse, HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.controllers.o_model import ModelUtils
from ontology.forms import ModelExportForm
from ontology.models import OModel
from ontology.plugins.json import GenericEncoder
from organisation.constants import TIME_SCHEDULE_NOW, TIME_SCHEDULE_SCHEDULED
from organisation.controllers.tasks import TaskController
from organisation.models import TASK_STATUS_SUCCESS, TASK_TYPE_EXPORT, Task


class ModelExportView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    form_class = ModelExportForm
    template_name = 'o_model/o_model_export.html'
    success_url = reverse_lazy('task_list')
    initial = {}
    permission_required = [('EXPORT', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        self.initial['model'] = self.kwargs.get('model_id')
        model = OModel.objects.get(id=self.initial['model'])
        form = self.form_class(initial=self.initial, user=self.request.user)
        return render(request, self.template_name, {'form': form, 'ontology_data': json.dumps(ModelUtils.ontology_to_dict(model=model), cls=GenericEncoder)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, user=self.request.user)
        model_id = kwargs.pop('model_id')
        model = OModel.objects.get(id=model_id)

        if form.is_valid():
            # <process form cleaned data>
            #model = form.cleaned_data.get('model')

            config = {
                'model_id': str(model.id),
                'format': form.cleaned_data.get('format'),
                'knowledge_set': form.cleaned_data.get('knowledge_set', 'instances'),
                'time_schedule': form.cleaned_data.get('time_schedule', TIME_SCHEDULE_SCHEDULED),

                'concept_ids': ModelUtils.process_POST_array(request.POST, 'concept_ids'),
                'relation_ids': ModelUtils.process_POST_array(request.POST, 'relation_ids'),
                'predicate_ids': ModelUtils.process_POST_array(request.POST, 'predicate_ids'),
                'instance_ids': ModelUtils.process_POST_array(request.POST, 'instance_ids')
            }

            t = Task.objects.create(
                name='export',
                description='',
                type=TASK_TYPE_EXPORT,
                config=json.dumps(config),
                user=self.request.user,
                organisation=model.organisation,
                created_by=self.request.user
            )
            t.save()
            
            if config.get("time_schedule") == TIME_SCHEDULE_NOW:
                
                TaskController.process_task(t)
                if t.status == TASK_STATUS_SUCCESS:
                    filename = t.attachment.file.name.split('/')[-1]
                    response = FileResponse(t.attachment, as_attachment=True, filename=filename)
                    if config.get('format') == 'json':
                        response["content-type"] = "application/json"
                    else:
                        response["content-type"] = 'text/plain'
                    return response
                else:
                    return HttpResponseBadRequest('Unable to process the task %s: %s' %(str(t.id), str(t.error)))

            elif config.get("time_schedule") == TIME_SCHEDULE_SCHEDULED:
                return HttpResponseRedirect(self.success_url)
            else:
                return HttpResponseBadRequest('Unknown time_schedule: '+ config.get("time_schedule"))

        return render(request, self.template_name, {'form': form, 'ontology_data': json.dumps(ModelUtils.ontology_to_dict(model=model), cls=GenericEncoder)})

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        return initials


