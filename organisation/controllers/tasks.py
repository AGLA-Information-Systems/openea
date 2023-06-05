
import json
import os
import traceback

from django.utils import timezone

from ontology.models import OModel
from ontology.plugins import EXPORTERS, IMPORTERS
from organisation.controllers.filestore import MediaFileStorage
from organisation.models import (TASK_PROCESSABLE_STATUSES,
                                 TASK_STATUS_FAILURE, TASK_STATUS_SUCCESS,
                                 TASK_TYPE_EXPORT, TASK_TYPE_IMPORT, Task)


class TaskController:
    def process_tasks(task_ids):
        processable_statuses = TASK_PROCESSABLE_STATUSES
        tasks = []
        if isinstance(task_ids, list):
            tasks = Task.objects.filter(pk__in=task_ids, status__in=processable_statuses).order_by('-created_at')
        if not tasks:
            tasks = Task.objects.filter(status__in=processable_statuses).order_by('-created_at')

        for task in tasks:
            TaskController.process_task(task)
            

    def process_task(task):
        try:
            task.started_at = timezone.now()
            result = TaskController.run_task(task=task)
            task.status = TASK_STATUS_SUCCESS
        except Exception as e:
            task.status = TASK_STATUS_FAILURE
            #task.error = traceback.format_exc()
            task.error = str(e)
        task.ended_at = timezone.now()
        task.save()


    def run_task(task):

        media_storage = MediaFileStorage()
        
        if task.type == TASK_TYPE_IMPORT:
            config = json.loads(task.config)

            model = OModel.objects.get(id=config['model_id'])
            TaskController.check_task_model_authorization(task=task, model=model)

            filename = os.path.basename(task.attachment.path)
            path = os.path.dirname(task.attachment.path)

            importer = IMPORTERS.get((config.get('format'), config.get('knowledge_set')))
            if importer is None:
                raise ValueError('IMPORTER_NOT_FOUND:{},{}'.format(config.get('format'), config.get('knowledge_set')))
            import_function = importer[0]
            file_extension = importer[1]

            import_function(model=model, path=path, filename=filename, filters=config)
            return task.attachment.name

            
        elif task.type == TASK_TYPE_EXPORT:
            config = json.loads(task.config)
            
            model = OModel.objects.get(id=config['model_id'])
            
            TaskController.check_task_model_authorization(task=task, model=model)

            path = media_storage.get_directory_path(task.organisation)
            if not os.path.exists(path.as_posix()):
                os.makedirs(path.as_posix())
            exporter = EXPORTERS.get((config.get('format'), config.get('knowledge_set')))
            if exporter is None:
                raise ValueError('EXPORTER_NOT_FOUND:{},{}'.format(config.get('format'), config.get('knowledge_set')))
            export_function = exporter[0]
            file_extension = exporter[1]
            
            path = media_storage.get_directory_path(organisation=task.organisation)
            filename = '{}-{}-{}.{}'.format(
                model.id, config.get('knowledge_set'),
                '{:%Y%m%d-%H%M%S}'.format(timezone.now()),
                file_extension)
 
            export_function(model=model, path=path, filename=filename, filters=config)
            task.attachment = str(media_storage.get_media_root_file_path(path / filename))
            return filename

        else:
            raise ValueError('UNEXPECTED_TASK_TYPE')


    def check_task_model_authorization(task, model):
        #TODO: User is admin? (only admin can create a task on behalf of another user)
        
        task_submitter = task.user or task.created_by
        user_is_authorized_in_organisation = False
        for profile in task_submitter.profiles.all():
            if profile.organisation == task.organisation:
                user_is_authorized_in_organisation = True

        if user_is_authorized_in_organisation == False:
            raise ValueError('UNAUTHORIZED_USER_IN_ORGANISATION:{},{}'.format(task_submitter.id, task.organisation.id))
        
        model_is_authorized_in_task = False
        if model.repository.organisation == task.organisation:
             model_is_authorized_in_task = True

        if  model_is_authorized_in_task == False:
            raise ValueError('UNAUTHORIZED_TASK_FOR_MODEL:{},{}'.format(task.id, model.id))
        return True
