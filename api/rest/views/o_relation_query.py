from rest_framework import permissions, generics
from ontology.models import ORelation, OModel
from api.rest.serializers import ORelationSerializer


class ORelationQueryView(generics.ListAPIView):
    serializer_class = ORelationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organisation = None
        if hasattr(self.request.user, 'organisation'):
            organisation = self.request.user.organisation
        model_id = self.kwargs['model_id']
        model = OModel.objects.get(organisation=organisation, id=model_id)
        queryset = ORelation.objects.filter(model=model)
        
        relation_name = self.request.query_params.get('name')
        if relation_name is not None:
            queryset = queryset.filter(name__icontains=relation_name)

        return queryset.order_by('-created_at')
