from django.core.management.base import BaseCommand
import imp
from unicodedata import name
from ontology.models import OModel, OConcept, OInstance, OPredicate, ORelation, Repository

class Command(BaseCommand):
    def handle(self, **options):
        orepository='Solution valuation'
        omodel='Solution expérience client'


        ontology_defs = [
        ('Solution Component', 'is-part-of', 'Solution'), 
        ('Project', 'is-part-of', 'Program'), 
        ('Solution Component', 'is-part-of', 'Solution Component'), 
        ('Solution Component', 'is-implemented-by', 'Work Package'), 
        ('Acquisition', 'is-part-of', 'Work Package'), 
        ('Operation', 'is-part-of', 'Work Package'), 
        ('Construction', 'is-part-of', 'Work Package'), 
        ('Decommission', 'is-part-of', 'Work Package'), 
        ('Conception', 'is-part-of', 'Work Package'), 
        ('Cost', 'is-a-property-of', 'Work Package'), 
        ('Cost', 'is-a-property-of', 'Resource'), 
        ('Work Package', 'is-implemented-by', 'Resource Allocation'), 
        ('Duration', 'is-a-property-of', 'Resource Allocation'), 
        ('Resource', 'is-a-property-of', 'Resource Allocation'), 
        ('Duration in Days', 'is-a-property-of', 'Duration'), 
        ('Duration in Hours', 'is-a-property-of', 'Duration'), 
        ('Duration in Weeks', 'is-a-property-of', 'Duration'), 
        ('Duration in Months', 'is-a-property-of', 'Duration'), 
        ('Duration in Years', 'is-a-property-of', 'Duration'), 
        ('Annual Cost', 'is-a-property-of', 'Cost'), 
        ('Quaterly Cost', 'is-a-property-of', 'Cost'), 
        ('Monthly Cost', 'is-a-property-of', 'Cost'), 
        ('Daily Cost', 'is-a-property-of', 'Cost'), 
        ('Duration in Quarters', 'is-a-property-of', 'Duration'), 
        ('Hourly Cost', 'is-a-property-of', 'Cost'), 
        ('Human Resource', 'is-a', 'Resource'), 
        ('Informational Resource', 'is-a', 'Resource'), 
        ('Computing Unit', 'is-a', 'Technology Component'), 
        ('Storage Unit', 'is-a', 'Technology Component'), 
        ('Networking Unit', 'is-a', 'Technology Component'), 
        ('Business Component', 'is-a', 'Solution Component'), 
        ('Application Component', 'is-a', 'Solution Component'), 
        ('Technology Component', 'is-a', 'Solution Component'), 
        ('Technology Component', 'is-a', 'Resource'), 
        ('Monitoring', 'is-part-of', 'Work Package'), 
        ('Start Date', 'is-a', 'Date'), 
        ('End Date', 'is-a', 'Date'), 
        ('Start Date', 'is-a-property-of', 'Resource Allocation'), 
        ('End Date', 'is-a-property-of', 'Resource Allocation'), 
        ('Work Package', 'is-dependant-on', 'Work Package'), 
        ('Start Date', 'is-a-property-of', 'Work Package'), 
        ('End Date', 'is-a-property-of', 'Work Package'), 
        ('Business Process', 'is-a', 'Business Component'),
        ('Objectif', 'is-a', 'Motivation Component'),
        ('Exigence Affaires', 'is-a', 'Business Component'),
        ('Exigence Affaires', 'serves', 'Objectif'), 
        ('Solution Component', 'fulfills', 'Exigence Affaires')
        ]

        instances = [
            ('Trajectoire Analytique Intelligence Client', 'Solution'),
            ('Fournir un rapport de performance des produits/services', 'Objectif'),
            ('Fournir un rapport de ciblage du marché', 'Objectif'),
            ('Fournir un rapport des parts de marché', 'Objectif'),

            ('Comptoir PowerBI - Performance des produits', 'Solution Component'),
            ('Comptoir PowerBI - Performance du ciblage', 'Solution Component'),
            ('Comptoir PowerBI - Parts de marché', 'Solution Component'), 

            ('Google Analytics', 'Technology Component'),
            ('Integration: Google Analytics - Azure Datalake ', 'Technology Component'),
            ('DialogInsight', 'Technology Component'),
            ('Integration: DialogInsight - Azure Datalake', 'Technology Component'),
            ('Moveit', 'Technology Component'),
            ('Azure Databricks', 'Technology Component'),
            ('Integration: Azure Datalake -  Azure Data Factory', 'Technology Component'),
            ('Azure Data Factory', 'Technology Component'),
            ('Integration: Azure Data Factory - Azure Databricks', 'Technology Component'),
            ('PowerBI', 'Technology Component'),
            ('Integration: Azure Databricks -  Power BI', 'Technology Component'),

            ('Ingestion de Google Analytics', 'Work Package'), 
            ('Ingestion de DialogInsight', 'Work Package'),
            ('Modelisation des données de Google Analytics', 'Work Package'), 
            ('Modelisation des données de DialogInsight', 'Work Package'),

            ('Creation du Comptoir PowerBI - Performance des produits', 'Work Package'), 
            ('Creation du Comptoir PowerBI - Performance du ciblage', 'Work Package'), 
            ('Creation du Comptoir PowerBI - Parts de marché', 'Work Package'),

            ('Allocation: Developpeur PowerBI - Creation du Comptoir PowerBI', 'Resource Allocation'),

            ('Developpeur PowerBI', 'Human Resource'),
            ('Developpeur Azure Data Factory', 'Human Resource'),
            ('Devleoppeur Databricks', 'Human Resource'),
            ('Developpeur Azure Stack', 'Human Resource'),
            ('Analyste Fonctionnel', 'Human Resource'),
            ('Architecte de solution', 'Human Resource')
        ]

        Slots = [

        ]

        repository = Repository.objects.get_or_create(name=orepository)[0]
        print(repository)
        model = OModel.objects.get_or_create(repository=repository, name=omodel)[0]
        print(model)

        for p in ontology_defs:
            print(p)
            c1 = OConcept.objects.get_or_create(model=model, name=p[0])[0]
            r1 = ORelation.objects.get_or_create(model=model, name=p[1])[0]
            c2 = OConcept.objects.get_or_create(model=model, name=p[2])[0]
            p1 = OPredicate.objects.get_or_create(model=model, subject=c1, relation=r1, object=c2)[0]

        for i in instances:
            print(i)
            c1 = OConcept.objects.get_or_create(model=model, name=i[1])[0]
            i1 = OInstance.objects.get_or_create(model=model, name=i[0], concept=c1)[0]
