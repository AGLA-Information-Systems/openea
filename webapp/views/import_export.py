import json
from authorization.controllers.utils import CustomPermissionRequiredMixin
from ontology.models import OModel

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy, reverse
from webapp.controllers.filestore import MediaFileStorage
from ..models import Organisation, TASK_TYPE_IMPORT, TASK_TYPE_EXPORT, Task

from ..forms import ModelExportForm, ModelImportForm
from ..utils import handle_uploaded_file

class ImportView(CustomPermissionRequiredMixin, View):
    form_class = ModelImportForm
    template_name = 'model_import.html'
    success_url = reverse_lazy('task_list')
    initial = {}
    permission_required = [('IMPORT', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        self.initial['model'] = self.kwargs.get('model_id')
        form = self.form_class(initial=self.initial, user=self.request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, user=self.request.user)
        if form.is_valid():
            # <process form cleaned data>
            media_storage = MediaFileStorage
            model = form.cleaned_data.get('model')
            organisation = model.repository.organisation

            #file_path = request.FILES['import_file'].path
            #handle_uploaded_file(request.FILES['import_file'])

            import_file = media_storage.store_file(organisation=organisation, uploaded_file=request.FILES['import_file'])
            config = {
                'model_id': str(model.id),
                'format': form.cleaned_data.get('import_format'),
                'knowledge_set': form.cleaned_data.get('knowledge_set'),
            }

            t = Task.objects.create(
                name='import',
                description='',
                type=TASK_TYPE_IMPORT,
                attachment=import_file,
                config=json.dumps(config),
                user=request.user,
                organisation=organisation)
            t.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})

class ExportView(CustomPermissionRequiredMixin, View):
    form_class = ModelExportForm
    template_name = 'model_export.html'
    success_url = reverse_lazy('task_list')
    initial = {}
    permission_required = [('EXPORT', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        self.initial['model'] = self.kwargs.get('model_id')
        form = self.form_class(initial=self.initial, user=self.request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, user=self.request.user)
        print(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            model = form.cleaned_data.get('model')
            config = {
                'model_id': str(model.id),
                'format': form.cleaned_data.get('export_format'),
                'knowledge_set': form.cleaned_data.get('knowledge_set'),
            }
            organisation = model.repository.organisation
            t = Task.objects.create(
                name='export',
                description='',
                type=TASK_TYPE_EXPORT,
                config=json.dumps(config),
                user=request.user,
                organisation=organisation
            )
            t.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    def get_initial(self):
        initials = super().get_initial()
        initials['model'] = self.kwargs.get('model_id')
        return initials

# class ImportExportView(View):
#     form_class = ImportExportForm
#     initial = {'key': 'value'}
#     template_name = 'import_export.html'
#     success_url = reverse_lazy('task_list')

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect(self.success_url)

#         return render(request, self.template_name, {'form': form})
