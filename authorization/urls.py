from django.urls import path


from authorization.views import PermissionDetailView
from authorization.views import PermissionListView

from authorization.views import SecurityGroupCreateView
from authorization.views import SecurityGroupDeleteView
from authorization.views import SecurityGroupDetailView
from authorization.views import SecurityGroupListOrganisationView, SecurityGroupListUserView, SecurityGroupListView
from authorization.views import SecurityGroupUpdateView

from authorization.views import AccessPermissionCreateView
from authorization.views import AccessPermissionDeleteView
from authorization.views import AccessPermissionDetailView
from authorization.views import AccessPermissionListOrganisationView, AccessPermissionListUserView, AccessPermissionListView
from authorization.views import AccessPermissionUpdateView

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
    path('permission/detail/<uuid:pk>/', PermissionDetailView.as_view(), name='permission_detail'),


    path('accesspermission/list/', AccessPermissionListView.as_view(), name='accesspermission_list'),
    path('accesspermission/list/<int:user_id>/', AccessPermissionListUserView.as_view(), name='accesspermission_list_user'),
    path('accesspermission/list/<uuid:organisation_id>/', AccessPermissionListOrganisationView.as_view(), name='accesspermission_list_organisation'),
    path('accesspermission/create/<int:user_id>/', AccessPermissionCreateView.as_view(), name='accesspermission_create_user'),
    path('accesspermission/create/<uuid:organisation_id>/', AccessPermissionCreateView.as_view(), name='accesspermission_create'),
    path('accesspermission/detail/<uuid:pk>/', AccessPermissionDetailView.as_view(), name='accesspermission_detail'),
    path('accesspermission/update/<uuid:pk>/', AccessPermissionUpdateView.as_view(), name='accesspermission_update'),
    path('accesspermission/delete/<uuid:pk>/', AccessPermissionDeleteView.as_view(), name='accesspermission_delete')
]