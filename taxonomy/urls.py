from django.urls import path

from taxonomy.views import TagCreateView
from taxonomy.views import TagDeleteView
from taxonomy.views import TagDetailView
from taxonomy.views import TagListOrganisationView, TagListUserView, TagListView
from taxonomy.views import TagUpdateView
from taxonomy.views import TagGroupCreateView
from taxonomy.views import TagGroupDeleteView
from taxonomy.views import TagGroupDetailView
from taxonomy.views import TagGroupListOrganisationView, TagGroupListUserView, TagGroupListView
from taxonomy.views import TagGroupUpdateView

urlpatterns = [
    path('tag_group/list/', TagGroupListView.as_view(), name='tag_group_list'),
    path('tag_group/list/<int:user_id>/', TagGroupListUserView.as_view(), name='tag_group_list_user'),
    path('tag_group/list/<uuid:organisation_id>/', TagGroupListOrganisationView.as_view(), name='tag_group_list_organisation'),
    path('tag_group/create/<int:user_id>/', TagGroupCreateView.as_view(), name='tag_group_create_user'),
    path('tag_group/create/<uuid:organisation_id>/', TagGroupCreateView.as_view(), name='tag_group_create'),
    path('tag_group/detail/<uuid:pk>/', TagGroupDetailView.as_view(), name='tag_group_detail'),
    path('tag_group/update/<uuid:pk>/', TagGroupUpdateView.as_view(), name='tag_group_update'),
    path('tag_group/delete/<uuid:pk>/', TagGroupDeleteView.as_view(), name='tag_group_delete'),
    
    path('tag/list/', TagListView.as_view(), name='tag_list'),
    path('tag/list/<int:user_id>/', TagListUserView.as_view(), name='tag_list_user'),
    path('tag/list/<uuid:organisation_id>/', TagListOrganisationView.as_view(), name='tag_list_organisation'),
    path('tag/create/<uuid:tag_group_id>/', TagCreateView.as_view(), name='tag_create'),
    path('tag/detail/<uuid:pk>/', TagDetailView.as_view(), name='tag_detail'),
    path('tag/update/<uuid:pk>/', TagUpdateView.as_view(), name='tag_update'),
    path('tag/delete/<uuid:pk>/', TagDeleteView.as_view(), name='tag_delete')
]