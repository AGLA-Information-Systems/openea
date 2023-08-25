import logging
from django.db import transaction
from django.core.management.base import BaseCommand

from ontology.models import OConcept, OInstance, OModel, OPredicate, ORelation, OReport, OSlot, Repository


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update organisation field'

    def add_arguments(self, parser):
        parser.add_argument('task_ids', nargs='*', type=str)

    def handle(self, *args, **options):
        with transaction.atomic():
            for repository in Repository.objects.all():
                self.stdout.write(self.style.SUCCESS('Repository "%s"' % (repository.name)))
                for model in OModel.objects.filter(repository=repository):
                    model.organisation = repository.organisation
                    model.save()
                    self.stdout.write(self.style.SUCCESS('OModel "%s"' % (model.name)))
                    for concept in OConcept.objects.filter(model=model):
                        concept.organisation = repository.organisation
                        concept.save()
                        self.stdout.write(self.style.SUCCESS('OConcept "%s"' % (concept.name)))
                    for instance in OInstance.objects.filter(model=model):
                        instance.organisation = repository.organisation
                        instance.save()
                        self.stdout.write(self.style.SUCCESS('OInstance "%s"' % (instance.name)))
                    for relation in ORelation.objects.filter(model=model):
                        relation.organisation = repository.organisation
                        relation.save()
                        self.stdout.write(self.style.SUCCESS('ORelation "%s"' % (relation.name)))
                    for predicate in OPredicate.objects.filter(model=model):
                        predicate.organisation = repository.organisation
                        predicate.save()
                        self.stdout.write(self.style.SUCCESS('OPredicate "%s"' % (predicate.name)))
                    for slot in OSlot.objects.filter(model=model):
                        slot.organisation = repository.organisation
                        slot.save()
                        self.stdout.write(self.style.SUCCESS('OSlot "%s"' % (slot.name)))
                    for report in OReport.objects.filter(model=model):
                        report.organisation = repository.organisation
                        report.save()
                        self.stdout.write(self.style.SUCCESS('OReport "%s"' % (report.name)))
