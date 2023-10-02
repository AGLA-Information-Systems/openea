from rest_framework import permissions, generics
from ontology.models import OModel, OPredicate
from api.rest.serializers import OPredicateSerializer


class OPredicateQueryView(generics.ListAPIView):
    serializer_class = OPredicateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organisation = None
        if hasattr(self.request.user, 'organisation'):
            organisation = self.request.user.organisation
        model_id = self.kwargs['model_id']
        model = OModel.objects.get(organisation=organisation, id=model_id)
        queryset = OPredicate.objects.filter(model=model)
        
        relation_name = self.request.query_params.get('relation_name')
        if relation_name is not None:
            queryset = queryset.filter(relation__name__icontains=relation_name)
        relation_id = self.request.query_params.get('relation_id')
        if relation_id is not None:
            queryset = queryset.filter(relation__id=relation_id)

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
