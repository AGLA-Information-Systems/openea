from django.urls import path

from authorization.views import PermissionCreateView
from authorization.views import PermissionDeleteView
from authorization.views import PermissionDetailView
from authorization.views import PermissionListOrganisationView, PermissionListUserView, PermissionListView
from authorization.views import PermissionUpdateView
from authorization.views import SecurityGroupCreateView
from authorization.views import SecurityGroupDeleteView
from authorization.views import SecurityGroupDetailView
from authorization.views import SecurityGroupListOrganisationView, SecurityGroupListUserView, SecurityGroupListView
from authorization.views import SecurityGroupUpdateView
from authorization.views.security_group.security_group_create import SecurityGroupAdminCreateView

urlpatterns = [
    path('security_group/list/', SecurityGroupListView.as_view(), name='security_group_list'),
    path('security_group/list/<int:user_id>/', SecurityGroupListUserView.as_view(), name='security_group_list_user'),
    path('security_group/list/<uuid:organisation_id>/', SecurityGroupListOrganisationView.as_view(), name='security_group_list_organisation'),
    path('security_group/create/<int:user_id>/', SecurityGroupCreateView.as_view(), name='security_group_create_user'),
    path('security_group/create/<uuid:organisation_id>/', SecurityGroupCreateView.as_view(), name='security_group_create'),
    path('security_group/detail/<uuid:pk>/', SecurityGroupDetailView.as_view(), name='security_group_detail'),
    path('security_group/update/<uuid:pk>/', SecurityGroupUpdateView.as_view(), name='security_group_update'),
    path('security_group/delete/<uuid:pk>/', SecurityGroupDeleteView.as_view(), name='security_group_delete'),
    path('security_group/rebuild_admin/<uuid:organisation_id>/', SecurityGroupAdminCreateView.as_view(), name='security_group_admin_rebuild'),
    
    path('permission/list/', PermissionListView.as_view(), name='permission_list'),
    path('permission/list/<int:user_id>/', PermissionListUserView.as_view(), name='permission_list_user'),
    path('permission/list/<uuid:organisation_id>/', PermissionListOrganisationView.as_view(), name='permission_list_organisation'),
    path('permission/create/<int:user_id>/', PermissionCreateView.as_view(), name='permission_create_user'),
    path('permission/create/<uuid:organisation_id>/', PermissionCreateView.as_view(), name='permission_create'),
    path('permission/detail/<uuid:pk>/', PermissionDetailView.as_view(), name='permission_detail'),
    path('permission/update/<uuid:pk>/', PermissionUpdateView.as_view(), name='permission_update'),
    path('permission/delete/<uuid:pk>/', PermissionDeleteView.as_view(), name='permission_delete')
]