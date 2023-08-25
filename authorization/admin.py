from django.contrib import admin
from authorization.models import AccessPermission, Permission, SecurityGroup


admin.site.register([Permission, AccessPermission, SecurityGroup])