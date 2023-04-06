from django.urls import path

from ontology.views import (
    OPredicateDeleteView, OPredicateUpdateView, OPredicateDetailView, OPredicateCreateView, OPredicateListView,
    ORelationDeleteView, ORelationUpdateView, ORelationDetailView, ORelationCreateView, ORelationListView,
    OConceptDeleteView, OConceptUpdateView, OConceptDetailView, OConceptCreateView, OConceptListView,
    OModelDeleteView, OModelUpdateView, OModelDetailView, OModelCreateView, OModelListView, OModelReportView,
    RepositoryDeleteView, RepositoryUpdateView, RepositoryDetailView, RepositoryCreateView, RepositoryListView
)
from ontology.views.import_export import ExportView, ImportView
from ontology.views.json_report import JSONReportView
from ontology.views.o_instance.o_instance_create import OInstanceCreateView
from ontology.views.o_instance.o_instance_delete import OInstanceDeleteView
from ontology.views.o_instance.o_instance_detail import OInstanceDetailView
from ontology.views.o_instance.o_instance_json_list import OInstanceJSONListView
from ontology.views.o_instance.o_instance_list import OInstanceListView
from ontology.views.o_instance.o_instance_update import OInstanceUpdateView
from ontology.views.o_model.o_model_json import OModelJSONView
from ontology.views.o_model.o_model_xml import OModelXMLView
from ontology.views.o_report.o_report_run import OReportRunView
from ontology.views.o_slot.o_slot_list import OSlotListView
from ontology.views.o_slot.o_slot_create import OSlotCreateView
from ontology.views.o_slot.o_slot_update import OSlotUpdateView
from ontology.views.o_slot.o_slot_delete import OSlotDeleteView
from ontology.views.o_slot.o_slot_detail import OSlotDetailView
from ontology.views.o_report.o_report_create import OReportCreateView
from ontology.views.o_report.o_report_delete import OReportDeleteView
from ontology.views.o_report.o_report_detail import OReportDetailView
from ontology.views.o_report.o_report_list import OReportListView
from ontology.views.o_report.o_report_update import OReportUpdateView
from ontology.views.report import ReportView
from ontology.views.xml_report import XMLReportView

urlpatterns = [
    path('repository/list/', RepositoryListView.as_view(), name='repository_list'),
    path('repository/create/', RepositoryCreateView.as_view(), name='repository_create'),
    path('repository/create/<uuid:organisation_id>/', RepositoryCreateView.as_view(), name='repository_create_organisation'),
    path('repository/detail/<uuid:pk>/', RepositoryDetailView.as_view(), name='repository_detail'),
    path('repository/update/<uuid:pk>/', RepositoryUpdateView.as_view(), name='repository_update'),
    path('repository/delete/<uuid:pk>/', RepositoryDeleteView.as_view(), name='repository_delete'),
    path('o_model/list/<uuid:repository_id>/', OModelListView.as_view(), name='o_model_list'),
    path('o_model/create/<uuid:repository_id>/', OModelCreateView.as_view(), name='o_model_create'),
    path('o_model/detail/<uuid:pk>/', OModelDetailView.as_view(), name='o_model_detail'),
    path('o_model/update/<uuid:pk>/', OModelUpdateView.as_view(), name='o_model_update'),
    path('o_model/delete/<uuid:pk>/', OModelDeleteView.as_view(), name='o_model_delete'),
    path('o_concept/list/<uuid:model_id>/', OConceptListView.as_view(), name='o_concept_list'),
    path('o_concept/create/<uuid:model_id>/', OConceptCreateView.as_view(), name='o_concept_create'),
    path('o_concept/detail/<uuid:pk>/', OConceptDetailView.as_view(), name='o_concept_detail'),
    path('o_concept/update/<uuid:pk>/', OConceptUpdateView.as_view(), name='o_concept_update'),
    path('o_concept/delete/<uuid:pk>/', OConceptDeleteView.as_view(), name='o_concept_delete'),
    path('o_relation/list/<uuid:model_id>/', ORelationListView.as_view(), name='o_relation_list'),
    path('o_relation/create/<uuid:model_id>/', ORelationCreateView.as_view(), name='o_relation_create'),
    path('o_relation/detail/<uuid:pk>/', ORelationDetailView.as_view(), name='o_relation_detail'),
    path('o_relation/update/<uuid:pk>/', ORelationUpdateView.as_view(), name='o_relation_update'),
    path('o_relation/delete/<uuid:pk>/', ORelationDeleteView.as_view(), name='o_relation_delete'),
    path('o_predicate/list/<uuid:model_id>/', OPredicateListView.as_view(), name='o_predicate_list'),
    path('o_predicate/create/<uuid:model_id>/', OPredicateCreateView.as_view(), name='o_predicate_create'),
    path('o_predicate/detail/<uuid:pk>/', OPredicateDetailView.as_view(), name='o_predicate_detail'),
    path('o_predicate/update/<uuid:pk>/', OPredicateUpdateView.as_view(), name='o_predicate_update'),
    path('o_predicate/delete/<uuid:pk>/', OPredicateDeleteView.as_view(), name='o_predicate_delete'),
    path('o_instance/list/<uuid:concept_id>/', OInstanceListView.as_view(), name='o_instance_list'),
    path('o_instance/json_list/<uuid:concept_id>/', OInstanceJSONListView.as_view(), name='o_instance_json_list'),
    path('o_instance/create/<uuid:concept_id>/', OInstanceCreateView.as_view(), name='o_instance_create'),
    path('o_instance/detail/<uuid:pk>/', OInstanceDetailView.as_view(), name='o_instance_detail'),
    path('o_instance/update/<uuid:pk>/', OInstanceUpdateView.as_view(), name='o_instance_update'),
    path('o_instance/delete/<uuid:pk>/', OInstanceDeleteView.as_view(), name='o_instance_delete'),
    path('o_slot/list/<uuid:instance_id>', OSlotListView.as_view(), name='o_slot_list'),
    path('o_slot/create/<uuid:instance_id>/<uuid:predicate_id>/<uuid:concept_id>/<is_subject>', OSlotCreateView.as_view(), name='o_slot_create'),
    path('o_slot/detail/<uuid:pk>/', OSlotDetailView.as_view(), name='o_slot_detail'),
    path('o_slot/update/<uuid:pk>/', OSlotUpdateView.as_view(), name='o_slot_update'),
    path('o_slot/delete/<uuid:pk>/', OSlotDeleteView.as_view(), name='o_slot_delete'),
    path('o_report/list/<uuid:model_id>/', OReportListView.as_view(), name='o_report_list'),
    path('o_report/create/<uuid:model_id>/', OReportCreateView.as_view(), name='o_report_create'),
    path('o_report/detail/<uuid:pk>/', OReportDetailView.as_view(), name='o_report_detail'),
    path('o_report/update/<uuid:pk>/', OReportUpdateView.as_view(), name='o_report_update'),
    path('o_report/delete/<uuid:pk>/', OReportDeleteView.as_view(), name='o_report_delete'),
    path('o_report/run/<uuid:pk>/', OReportRunView.as_view(), name='o_report_run'),

    path('o_model/report/<uuid:pk>/', OModelReportView.as_view(), name='o_model_report'),
    path('o_model_xml/<uuid:model_id>/', OModelXMLView.as_view(), name='o_model_xml'),
    path('o_model_json/<uuid:model_id>/', OModelJSONView.as_view(), name='o_model_json'),

    path('model_import/<uuid:model_id>/', ImportView.as_view(), name='model_import'),
    path('model_export/<uuid:model_id>/', ExportView.as_view(), name='model_export'),
    path('model_report/<uuid:model_id>/', ReportView.as_view(), name='model_report'),
    path('xml_report/<uuid:model_id>/', XMLReportView.as_view(), name='xml_report'),
    path('json_report/<uuid:model_id>/', JSONReportView.as_view(), name='json_report')
]