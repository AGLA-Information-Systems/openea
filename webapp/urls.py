from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from webapp.views.index import index, register

from webapp.views.others.about import AboutView


urlpatterns = [
    path('', index, name='index'),
    path('user/', include('django.contrib.auth.urls')),
    path("register/", register, name="register"),

    path('about/features', AboutView.as_view(), name='features'),
    path('about/resources', AboutView.as_view(), name='resources'),
    path('about/terms', AboutView.as_view(), name='terms'),
    path('about/privacy', AboutView.as_view(), name='privacy')
]