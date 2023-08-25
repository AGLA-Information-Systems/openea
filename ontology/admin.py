from django.contrib import admin
from ontology.models import OConcept, OInstance, OModel, OPredicate, ORelation, OReport, OSlot, Repository


admin.site.register([Repository, OModel, OConcept, ORelation, OPredicate, OInstance, OSlot, OReport])
