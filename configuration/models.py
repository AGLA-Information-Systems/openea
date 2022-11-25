import uuid
from django.db import models

from openea.utils import Utils
from webapp.models import Organisation


class Configuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    content = models.JSONField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_configurations')


    def get_or_create(organisation, name, content=None):
        try:
            configuration = Configuration.objects.get(organisation=organisation, name=name)
        except:
            configuration = Configuration.objects.create(organisation=organisation, name=name, content=content)
            configuration.save()
        return configuration

    def get_organisation(self):
        return self.organisation

    def get_object_type():
        return Utils.OBJECT_CONFIG

    def __str__(self):
        return self.name
