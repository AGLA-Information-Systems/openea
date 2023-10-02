from rest_framework import permissions, generics
from ontology.models import OInstance, OModel
from api.rest.serializers import OInstanceSerializer


class OInstanceQueryView(generics.ListAPIView):
    serializer_class = OInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organisation = None
        if hasattr(self.request.user, 'organisation'):
            organisation = self.request.user.organisation
        model_id = self.kwargs['model_id']
        model = OModel.objects.get(organisation=organisation, id=model_id)
        queryset = OInstance.objects.filter(model=model)
        
        instance_name = self.request.query_params.get('name')
        if instance_name is not None:
            queryset = queryset.filter(name__icontains=instance_name)

        concept_name = self.request.query_params.get('concept_name')
        if concept_name is not None:
            queryset = queryset.filter(concept__name__icontains=concept_name)

        concept_id = self.request.query_params.get('concept_id')
        if concept_id is not None:
            queryset = queryset.filter(concept__id=concept_id)
        return queryset.order_by('-created_at')
