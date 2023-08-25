from django.contrib import admin

from organisation.models import Organisation, Profile, Task

admin.site.register([Organisation, Profile, Task])
