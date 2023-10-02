from rest_framework import viewsets
from rest_framework import permissions
from ontology.models import Organisation
from api.rest.serializers import OrganisationSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Organisation.objects.all().order_by('-created_at')
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]