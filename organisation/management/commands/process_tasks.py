import os
import traceback
import json
import threading
import logging
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from organisation.models import TASK_STATUS_FAILURE, TASK_STATUS_SUCCESS, Task, TASK_PROCESSABLE_STATUSES, TASK_TYPE_IMPORT, TASK_TYPE_EXPORT
from ontology.controllers.knowledge_base import KnowledgeBaseController
from webapp.controllers.filestore import MediaFileStorage
from ontology.plugins import IMPORTERS, EXPORTERS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Closes the specified task for voting'

    def add_arguments(self, parser):
        #parser.add_argument('task_ids', nargs='+', type=int)
        parser.add_argument('task_ids', nargs='*', type=str)

    def handle(self, *args, **options):
        processable_statuses = TASK_PROCESSABLE_STATUSES
        tasks = []
        if 'task_ids' in options:
            task_ids = options['task_ids']
            if isinstance(task_ids, list):
                tasks = Task.objects.filter(pk__in=task_ids, status__in=processable_statuses).order_by('-created_at')
        if not tasks:
            tasks = Task.objects.filter(status__in=processable_statuses).order_by('-created_at')

        for task in tasks:
            self.process_task(task)
            #t = threading.Thread(target=Command.process_task, args=[self, task])
            #t.setDaemon(True)
            #t.start()
            

    def process_task(self, task):
        self.stdout.write(self.style.NOTICE('Started task "%s:%s"' % (task.id, task.name)))
        try:
            task.started_at = timezone.now()
            result = Command.run_task(task=task)
            task.status = TASK_STATUS_SUCCESS
            self.stdout.write(self.style.SUCCESS('Successfully closed task "%s:%s"' % (task.id, task.name)))
            task.error = None
        except Exception as e:
            task.status = TASK_STATUS_FAILURE
            task.error = traceback.format_exc()
            self.stdout.write(self.style.ERROR('Unable to process task "%s(%s):%s"' % (task.id, task.name, str(e))))
            logger.error("{} {}: {}".format(task.id, task.name, task.error))
        task.ended_at = timezone.now()
        task.save()


    def run_task(task):

        media_storage = MediaFileStorage()
        
        if task.type == TASK_TYPE_IMPORT:
            config = json.loads(task.config)

            model = KnowledgeBaseController.get_model(id=config['model_id'])
            Command.check_task_model_authorization(task=task, model=model)

            filename = os.path.basename(task.attachment.path)
            path = os.path.dirname(task.attachment.path)

            importer = IMPORTERS.get((config.get('format'), config.get('knowledge_set')))
            if importer is None:
                raise CommandError('IMPORTER_NOT_FOUND:{},{}'.format(config.get('format'), config.get('knowledge_set')))
            export_function = importer[0]
            file_extension = importer[1]

            export_function(model=model, path=path, filename=filename)
            return task.attachment.name

            
        elif task.type == TASK_TYPE_EXPORT:
            config = json.loads(task.config)
            
            model = KnowledgeBaseController.get_model(id=config['model_id'])
            
            Command.check_task_model_authorization(task=task, model=model)

            path = media_storage.get_directory_path(task.organisation)
            if not os.path.exists(path.as_posix()):
                os.makedirs(path.as_posix())
            exporter = EXPORTERS.get((config.get('format'), config.get('knowledge_set')))
            if exporter is None:
                raise CommandError('EXPORTER_NOT_FOUND:{},{}'.format(config.get('format'), config.get('knowledge_set')))
            export_function = exporter[0]
            file_extension = exporter[1]
            
            path = media_storage.get_directory_path(organisation=task.organisation)
            filename = '{}-{}-{}.{}'.format(
                model.id, config.get('knowledge_set'),
                '{:%Y%m%d-%H%M%S}'.format(timezone.now()),
                file_extension)
 
            export_function(model=model, path=path, filename=filename)
            task.attachment = str(media_storage.get_media_root_file_path(path / filename))
            return filename

        else:
            raise CommandError('UNEXPECTED_TASK_TYPE')


    def check_task_model_authorization(task, model):
        #TODO: User is admin? (only admin can create a task on behalf of another user)
        
        task_submitter = task.user or task.created_by
        user_is_authorized_in_organisation = False
        for profile in task_submitter.profiles.all():
            if profile.organisation == task.organisation:
                user_is_authorized_in_organisation = True

        if user_is_authorized_in_organisation == False:
            raise CommandError('UNAUTHORIZED_USER_IN_ORGANISATION:{},{}'.format(task_submitter.id, task.organisation.id))
        
        model_is_authorized_in_task = False
        if model.repository.organisation == task.organisation:
             model_is_authorized_in_task = True

        if  model_is_authorized_in_task == False:
            raise CommandError('UNAUTHORIZED_TASK_FOR_MODEL:{},{}'.format(task.id, model.id))
        return True
