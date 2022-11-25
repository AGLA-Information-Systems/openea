from django.urls import path
from configuration.views import ConfigurationListView, ConfigurationCreateView, ConfigurationRebuildView, ConfigurationUpdateView, ConfigurationDeleteView, ConfigurationDetailView, ConfigurationListOrganisationView, ConfigurationListUserView


urlpatterns = [
    path('configuration/list/', ConfigurationListView.as_view(), name='configuration_list'),
    path('configuration/list/<int:user_id>/', ConfigurationListUserView.as_view(), name='configuration_list_user'),
    path('configuration/list/<uuid:organisation_id>/', ConfigurationListOrganisationView.as_view(), name='configuration_list_organisation'),
    path('configuration/create/<int:user_id>/', ConfigurationCreateView.as_view(), name='configuration_create_user'),
    path('configuration/create/<uuid:organisation_id>/', ConfigurationCreateView.as_view(), name='configuration_create'),
    path('configuration/detail/<uuid:pk>/', ConfigurationDetailView.as_view(), name='configuration_detail'),
    path('configuration/update/<uuid:pk>/', ConfigurationUpdateView.as_view(), name='configuration_update'),
    path('configuration/delete/<uuid:pk>/', ConfigurationDeleteView.as_view(), name='configuration_delete'),

    path('configuration/rebuild/<uuid:organisation_id>/', ConfigurationRebuildView.as_view(), name='configuration_rebuild')
]