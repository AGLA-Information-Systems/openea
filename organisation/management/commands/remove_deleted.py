import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from ontology.models import (OConcept, OInstance, OModel, OPredicate,
                             ORelation, OReport, OSlot, Repository)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Remove definitely deleted data'

    def add_arguments(self, parser):
        parser.add_argument('items_ids', nargs='*', type=str)

    def handle(self, *args, **options):
        with transaction.atomic():
            classes = [Repository, OModel, OConcept, ORelation, OPredicate, OInstance, OSlot, OReport]
            for item_class in classes:
                for item_instance in item_class.objects.filter(deleted_at__isnull=False):
                    item_instance.delete()
                    self.stdout.write(self.style.SUCCESS('Class "%s" - Instance "%s"' % (item_class.__name__, item_instance)))

