from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from api.rest.serializers import ORelationSerializer
from ontology.models import OModel, ORelation


class ORelationRetriveView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ORelation.objects.all().order_by('-created_at')
    serializer_class = ORelationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organisation = None
        if hasattr(self.request.user, 'organisation'):
            organisation = self.request.user.organisation
        model_id = self.kwargs['model_id']
        model = OModel.objects.get(organisation=organisation, id=model_id)
        queryset = ORelation.objects.filter(model=model)
        return queryset
