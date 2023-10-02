from rest_framework import viewsets
from rest_framework import permissions
from ontology.models import OModel
from api.rest.serializers import OModelSerializer


class OModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = OModel.objects.all().order_by('-created_at')
    serializer_class = OModelSerializer
    permission_classes = [permissions.IsAuthenticated]