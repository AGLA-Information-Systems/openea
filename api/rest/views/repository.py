from rest_framework import viewsets
from rest_framework import permissions
from ontology.models import Repository
from api.rest.serializers import RepositorySerializer


class RepositoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Repository.objects.all().order_by('-created_at')
    serializer_class = RepositorySerializer
    permission_classes = [permissions.IsAuthenticated]