from django.shortcuts import render
from django.views.generic import View
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

from ontology.models import OConcept, OInstance, OModel, OPredicate, OSlot


class OModelXMLView(CustomPermissionRequiredMixin, View):
    permission_required = [('VIEW', OModel.get_object_type(), None)]

    def get(self, request, *args, **kwargs):
        model_id = kwargs.pop('model_id')
        model = OModel.objects.get(id=model_id)
        predicates = OPredicate.objects.filter(model=model).order_by('-subject').all()
        entities = OConcept.objects.filter(model=model).order_by('-name').all()
        instances = OInstance.objects.filter(model=model).order_by('-name').all()
        ownslots = {}
        for x in instances:
            ownslots[x.id] = OSlot.objects.filter(model=model, subject=x).all()
        inslots = {}
        for x in instances:
            inslots[x.id] = OSlot.objects.filter(model=model, object=x).all()

        return render(request, 'o_model/o_model_xml.html',
                        {
                            'model': model,
                            'predicates': predicates,
                            'entities': entities,
                            'instances': instances,
                            'ownslots': ownslots,
                            'inslots': inslots
                        }, content_type="application/xhtml+xml")
