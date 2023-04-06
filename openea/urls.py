"""openea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('webapp.urls'), name="webapp"),
]

urlpatterns += [
    path('', include('organisation.urls'), name="organisation"),
    path('', include('ontology.urls'), name="ontology"),
    path('', include('authentication.urls'), name="authentication"),
    path('', include('authorization.urls'), name="authorization"),
    path('', include('taxonomy.urls'), name="taxonomy"),
    path('', include('configuration.urls'), name="configuration"),

    path('', include('pagedown.urls')),

    path('i18n/', include('django.conf.urls.i18n')),
    path('select2/', include('django_select2.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
