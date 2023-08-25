import uuid
from django.db import models
from django.contrib.auth.models import User
from organisation.models import Organisation

class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=1024, blank=True, null=True)
    target = models.UUIDField(blank=True, null=True)
    uri = models.CharField(max_length=1024, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True) #  IPv4-mapped IPv6 address (https://www.rfc-editor.org/rfc/rfc4291#section-2.5.5.2)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='user_logs')
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT, null=True, related_name='organisation_logs')

    def get_organisation(self):
        return self.organisation
    
    def filter_by_organisation(organisation):
        return Log.objects.filter(organisation=organisation)
     
    def __str__(self):
        return self.name
