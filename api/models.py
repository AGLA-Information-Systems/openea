import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from organisation.models import Organisation

User = get_user_model()

class APIKey(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=4096)
    secret = models.CharField(max_length=4096)
    active = models.BooleanField(default=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_apikeys')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='apikey_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='apikey_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='apikey_deleted')
    
    def __str__(self):
        return "{}:{}".format(self.organisation.name, self.key)
