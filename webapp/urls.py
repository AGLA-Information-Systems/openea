from django.urls import path
from webapp.views.index import index
from webapp.views.others.about import AboutView


urlpatterns = [
    path('', index, name='index'),

    path('about/features', AboutView.as_view(), name='features'),
    path('about/resources', AboutView.as_view(), name='resources'),
    path('about/terms', AboutView.as_view(), name='terms'),
    path('about/privacy', AboutView.as_view(), name='privacy')
]