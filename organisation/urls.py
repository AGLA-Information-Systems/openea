from django.urls import path, include

from organisation.views.organisation import (
    OrganisationListView,
    OrganisationCreateView,
    OrganisationDetailView,
    OrganisationUpdateView,
    OrganisationDeleteView,
    OrganisationListUserView,
)

from organisation.views.profile import (
    ProfileListView,
    ProfileCreateView,
    ProfileDetailView,
    ProfileUpdateView,
    ProfileDeleteView,
    ProfileListOrganisationView,
    ProfileListUserView,
    ProfileActivateView
)
from organisation.views.task import (
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListOrganisationView,
    TaskListUserView
)


urlpatterns = [

    path('organisation/list/', OrganisationListView.as_view(), name='organisation_list'),
    path('organisation/list/<int:user_id>/', OrganisationListUserView.as_view(), name='organisation_list_user'),
    path('organisation/create/', OrganisationCreateView.as_view(), name='organisation_create'),
    path('organisation/detail/<uuid:pk>/', OrganisationDetailView.as_view(), name='organisation_detail'),
    path('organisation/update/<uuid:pk>/', OrganisationUpdateView.as_view(), name='organisation_update'),
    path('organisation/delete/<uuid:pk>/', OrganisationDeleteView.as_view(), name='organisation_delete'),

    path('profile/list/', ProfileListView.as_view(), name='profile_list'),
    path('profile/list/<int:user_id>/', ProfileListUserView.as_view(), name='profile_list_user'),
    path('profile/list/<uuid:organisation_id>/', ProfileListOrganisationView.as_view(), name='profile_list_organisation'),
    path('profile/create/<int:user_id>/', ProfileCreateView.as_view(), name='profile_create_user'),
    path('profile/create/<uuid:organisation_id>/', ProfileCreateView.as_view(), name='profile_create'),
    path('profile/detail/<uuid:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/<uuid:pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/delete/<uuid:pk>/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('profile/activate/<uuid:pk>/', ProfileActivateView.as_view(), name='profile_activate'),

    path('task/list/', TaskListView.as_view(), name='task_list'),
    path('task/list/<int:user_id>/', TaskListUserView.as_view(), name='task_list_user'),
    path('task/list/<uuid:organisation_id>/', TaskListOrganisationView.as_view(), name='task_list_organisation'),
    path('task/create/<int:user_id>/', TaskCreateView.as_view(), name='task_create_user'),
    path('task/create/<uuid:organisation_id>/', TaskCreateView.as_view(), name='task_create'),
    path('task/detail/<uuid:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/update/<uuid:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/<uuid:pk>/', TaskDeleteView.as_view(), name='task_delete'),

]