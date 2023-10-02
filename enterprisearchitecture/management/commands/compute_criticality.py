import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from openpyxl import load_workbook

from ontology.models import (OConcept, OInstance, OModel, OPredicate,
                             ORelation, OSlot)


class Command(BaseCommand):
    help = 'Create an model with its permissions'

    def add_arguments(self, parser):
        parser.add_argument('model_name', nargs=1, type=str)
        parser.add_argument('model_version', nargs=1, type=str)

    def handle(self, *args, **options):
        model_name = options['model_name'][0]
        model_version = options['model_version'][0]
        
        with transaction.atomic():
            try:
                model = OModel.objects.get(name=model_name, version=model_version)
                print(model.id)
                property_relation = ORelation.objects.get(model=model, name='a pour propriété')
                support_relation = ORelation.objects.get(model=model, name='supporte')
                realize_relation = ORelation.objects.get(model=model, name='realize')
                
                criticality_concept = OConcept.objects.get(model=model, name='Criticité')
                value_stream_concept = OConcept.objects.get(model=model, name='Flux de valeur')
                capability_concept = OConcept.objects.get(model=model, name="Capacité d'affaires")
                product_concept = OConcept.objects.get(model=model, name='Produit')
                process_concept = OConcept.objects.get(model=model, name='Processus')
                application_concept = OConcept.objects.get(model=model, name='Système informatique ou Outil')
                instance_application_concept = OConcept.objects.get(model=model, name='Instance de Système informatique')


                capability_criticality_predicate = OPredicate.objects.get(model=model, subject=capability_concept, relation=property_relation, object=criticality_concept)

                capability_value_stream_predicate = OPredicate.objects.get(model=model, subject=capability_concept, relation=support_relation, object=value_stream_concept)
                product_capability_predicate = OPredicate.objects.get(model=model, subject=product_concept, relation=support_relation, object=capability_concept)
                process_product_predicate = OPredicate.objects.get(model=model, subject=process_concept, relation=support_relation, object=product_concept)
                application_process_predicate = OPredicate.objects.get(model=model, subject=application_concept, relation=support_relation, object=process_concept)

                application_criticality_predicate = OPredicate.objects.get(model=model, subject=application_concept, relation=property_relation, object=criticality_concept)

                criticality = None
                for capability in OInstance.objects.filter(model=model, concept=capability_concept).all():
                    for product in [x.subject for x in OSlot.objects.filter(predicate=product_capability_predicate, object=capability)]:
                        for process in [x.subject for x in OSlot.objects.filter(predicate=process_product_predicate, object=product)]:
                            for application in [x.subject for x in OSlot.objects.filter(predicate=application_process_predicate, object=process)]:
                                criticalities = [x.object for x in OSlot.objects.filter(predicate=application_criticality_predicate, subject=application)]
                                criticality = Command.get_best_criticality(criticalities);


                            slot = OSlot.objects.get_or_create(model=model, subject=process, predicate=process_criticality_predicate, object=criticality)
                        slot = OSlot.objects.get_or_create(model=model, subject=product, predicate=product_criticality_predicate, object=criticality)
                    slot = OSlot.objects.get_or_create(model=model, subject=capability, predicate=capability_criticality_predicate, object=criticality)
                
                
                self.stdout.write(self.style.SUCCESS('Successfully updated model "%s"' % model_name))

            except Exception as e:
                #self.stdout.write(self.style.ERROR('Unable to update model "%s": %s' % (model_name, str(e))))
                raise CommandError('Unable to update model "%s": %s' % (model_name, str(e)))
    
    def get_best_criticality():
        return None