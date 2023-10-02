from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import routers

from api.rest import views
from api.rest.views.o_concept_detail import OConceptRetriveView
from api.rest.views.o_concept_query import OConceptQueryView
from api.rest.views.o_instance_detail import OInstanceRetriveView
from api.rest.views.o_instance_query import OInstanceQueryView
from api.rest.views.o_predicate_detail import OPredicateRetriveView
from api.rest.views.o_predicate_query import OPredicateQueryView
from api.rest.views.o_relation_detail import ORelationRetriveView
from api.rest.views.o_relation_query import ORelationQueryView
from api.rest.views.o_slot_detail import OSlotRetriveView
from api.rest.views.o_slot_query import OSlotQueryView

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'organisations', views.OrganisationViewSet)
router.register(r'repositories', views.RepositoryViewSet)
router.register(r'models', views.OModelViewSet)
router.register(r'concepts', views.OConceptViewSet)
router.register(r'relations', views.ORelationViewSet)
router.register(r'predicates', views.OPredicateViewSet)
router.register(r'instances', views.OInstanceViewSet)
router.register(r'slots', views.OSlotViewSet)

urlpatterns = [
    
    path('rest/model/<uuid:model_id>/concepts/<uuid:pk>', OConceptRetriveView.as_view(), name='model_concept'),
    path('rest/model/<uuid:model_id>/relations/<uuid:pk>', ORelationRetriveView.as_view(), name='model_relation'),
    path('rest/model/<uuid:model_id>/predicates/<uuid:pk>', OPredicateRetriveView.as_view(), name='model_predicate'),
    path('rest/model/<uuid:model_id>/instances/<uuid:pk>', OInstanceRetriveView.as_view(), name='model_instance'),
    path('rest/model/<uuid:model_id>/slots/<uuid:pk>', OSlotRetriveView.as_view(), name='model_slot'),

    path('rest/model/<uuid:model_id>/concepts/', OConceptQueryView.as_view(), name='model_concepts'),
    path('rest/model/<uuid:model_id>/relations/', ORelationQueryView.as_view(), name='model_relations'),
    path('rest/model/<uuid:model_id>/predicates/', OPredicateQueryView.as_view(), name='model_predicates'),
    path('rest/model/<uuid:model_id>/instances/', OInstanceQueryView.as_view(), name='model_instances'),
    path('rest/model/<uuid:model_id>/slots/', OSlotQueryView.as_view(), name='model_slots'),

    path('token/', views.ObtainTokenView.as_view(), name='token'),
    path('token/refresh', views.RefreshTokenView.as_view(), name='token'),
    path('rest/', include(router.urls)),
    path('rest/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)))
]
