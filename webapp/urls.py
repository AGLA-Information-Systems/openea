from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from webapp.views.index import index, register
from webapp.views.import_export import ImportView, ExportView
from webapp.views.json_report import JSONReportView

from webapp.views.organisation import (
    OrganisationListView,
    OrganisationCreateView,
    OrganisationDetailView,
    OrganisationUpdateView,
    OrganisationDeleteView,
    OrganisationListUserView,
)
from webapp.views.others.about import AboutView
from webapp.views.profile import (
    ProfileListView,
    ProfileCreateView,
    ProfileDetailView,
    ProfileUpdateView,
    ProfileDeleteView,
    ProfileListOrganisationView,
    ProfileListUserView,
    ProfileActivateView
)
from webapp.views.report import ReportView
from webapp.views.task import (
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListOrganisationView,
    TaskListUserView
)
from webapp.views.xml_report import XMLReportView


urlpatterns = [
    path('', index, name='index'),
    path('user/', include('django.contrib.auth.urls')),
    path("register/", register, name="register"),
    #path('imp_exp/<uuid:model_id>/', ImportExportView.as_view(), name='import_export'),
    path('model_import/<uuid:model_id>/', ImportView.as_view(), name='model_import'),
    path('model_export/<uuid:model_id>/', ExportView.as_view(), name='model_export'),
    path('model_report/<uuid:model_id>/', ReportView.as_view(), name='model_report'),

    path('xml_report/<uuid:model_id>/', XMLReportView.as_view(), name='xml_report'),
    path('json_report/<uuid:model_id>/', JSONReportView.as_view(), name='json_report'),
    
    path('organisation/list/', OrganisationListView.as_view(), name='organisation_list'),
    path('organisation/list/<int:user_id>/', TaskListUserView.as_view(), name='organisation_list_user'),
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

    path('about/features', AboutView.as_view(), name='features'),
    path('about/resources', AboutView.as_view(), name='resources'),
    path('about/terms', AboutView.as_view(), name='terms'),
    path('about/privacy', AboutView.as_view(), name='privacy')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)