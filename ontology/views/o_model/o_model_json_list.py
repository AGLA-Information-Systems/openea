import json
from django.http import HttpResponse
from django.views.generic import View
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OConcept, OInstance, OModel, OPredicate, ORelation
from ontology.plugins.json import GenericEncoder


class OModelJSONListView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    model = OModel
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        models = OModel.objects.order_by('name')
        data = {}
        for model in models:
            data[str(model.id)] = {
                "id": model.id,
                "name": model.name,
                "concepts": {},
                "relations": {},
                "predicates": {},
                "instances": {},
            }
            for concept in OConcept.objects.filter(model=model).order_by('name'):
                data[str(model.id)]["concepts"][str(concept.id)] = {
                    "id": concept.id,
                    "name": concept.name,
                }
            for relation in ORelation.objects.filter(model=model).order_by('name'):
                data[str(model.id)]["relations"][str(relation.id)] = {
                    "id": relation.id,
                    "name": relation.name,
                }
            for predicate in OPredicate.objects.filter(model=model).order_by('object__name').order_by('relation__name').order_by('subject__name'):
                data[str(model.id)]["predicates"][str(predicate.id)] = {
                    "id": predicate.id,
                    "subject": predicate.subject.name,
                    "relation": predicate.relation.name,
                    "object": predicate.object.name,
                }
            for instance in OInstance.objects.filter(model=model).order_by('name'):
                data[str(model.id)]["instances"][str(instance.id)] = {
                    "id": instance.id,
                    "name": instance.name,
                }
        return HttpResponse(json.dumps(data, cls=GenericEncoder), content_type="application/json")