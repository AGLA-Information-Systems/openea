from rest_framework import permissions, generics
from ontology.models import OModel, OSlot
from api.rest.serializers import OSlotSerializer


class OSlotQueryView(generics.ListAPIView):
    serializer_class = OSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organisation = None
        if hasattr(self.request.user, 'organisation'):
            organisation = self.request.user.organisation
        model_id = self.kwargs['model_id']
        model = OModel.objects.get(organisation=organisation, id=model_id)
        queryset = OSlot.objects.filter(model=model)
        
        slot_name = self.request.query_params.get('name')
        if slot_name is not None:
            queryset = queryset.filter(name__icontains=slot_name)
        
        predicate_name = self.request.query_params.get('predicate_name')
        if predicate_name is not None:
            queryset = queryset.filter(predicate__name__icontains=predicate_name)
        predicate_id = self.request.query_params.get('predicate_id')
        if predicate_id is not None:
            queryset = queryset.filter(predicate__id=predicate_id)

        subject_name = self.request.query_params.get('subject_name')
        if subject_name is not None:
            queryset = queryset.filter(subject__name__icontains=subject_name)
        subject_id = self.request.query_params.get('subject_id')
        if subject_id is not None:
            queryset = queryset.filter(subject__id=subject_id)

        object_name = self.request.query_params.get('object_name')
        if object_name is not None:
            queryset = queryset.filter(object__name__icontains=object_name)
        object_id = self.request.query_params.get('object_id')
        if object_id is not None:
            queryset = queryset.filter(object__id=object_id)

        return queryset.order_by('-created_at')
