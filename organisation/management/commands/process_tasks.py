import json
import logging
import os
import threading
import traceback

from django.core.management.base import BaseCommand
from django.utils import timezone

from organisation.controllers.tasks import TaskController
from organisation.models import (TASK_PROCESSABLE_STATUSES,
                                 TASK_STATUS_FAILURE, TASK_STATUS_SUCCESS,
                                 Task)

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
            result = TaskController.run_task(task=task)
            task.status = TASK_STATUS_SUCCESS
            self.stdout.write(self.style.SUCCESS('Successfully closed task "%s:%s"' % (task.id, task.name)))
            task.error = None
        except Exception as e:
            task.status = TASK_STATUS_FAILURE
            task.error = str(e)
            self.stdout.write(self.style.ERROR('Unable to process task "%s(%s):%s"' % (task.id, task.name, traceback.format_exc())))
            logger.error("{} {}: {}".format(task.id, task.name, traceback.format_exc()))
        task.ended_at = timezone.now()
        task.save()
