from rest_framework import viewsets
from rest_framework import permissions
from ontology.models import OConcept, OModel
from api.rest.serializers import OConceptSerializer


class OConceptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = OConcept.objects.all().order_by('-created_at')
    serializer_class = OConceptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organisation = None
        if hasattr(self.request.user, 'organisation'):
            organisation = self.request.user.organisation
        model_id = self.kwargs['model_id']
        model = OModel.objects.get(organisation=organisation, id=model_id)
        queryset = OConcept.objects.filter(model=model)
    
        concept_name = self.request.query_params.get('name')
        if concept_name is not None:
            queryset = queryset.filter(name__icontains=concept_name)

        return queryset.order_by('-created_at')
