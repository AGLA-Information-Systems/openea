from django.contrib import admin
from taxonomy.models import Tag, TagGroup


admin.site.register([TagGroup, Tag])
