import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from openea.utils import Utils
from organisation.models import Organisation, OrganisationManager, Profile
from utils.generic import GenericModel


class Permission(GenericModel, models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=10, choices=Utils.PERMISSION_ACTION, default=Utils.PERMISSION_ACTION_VIEW)  
    object_type = models.CharField(max_length=50)

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='permission_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='permission_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='permission_deleted')
     
    def __str__(self):
        return "{}:{}".format(self.action, self.object_type)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_permission_per_system',
                fields=['action', 'object_type'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]


class AccessPermission(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    object_identifier = models.UUIDField(blank=True, null=True)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True, related_name='permission_accesspermissions')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_accesspermissions')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='accesspermission_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='accesspermission_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='accesspermission_deleted')

    objects = OrganisationManager()
     
    def __str__(self):
        return "{}:{}".format(self.organisation, self.permission)
    

class SecurityGroup(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    profiles = models.ManyToManyField(Profile, related_name='security_groups')
    accesspermissions = models.ManyToManyField(AccessPermission, related_name='security_group_accesspermissions')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_security_groups')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='security_group_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='security_group_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='security_group_deleted')

    def get_or_create(name, organisation, description=''):
        try:
            security_group = SecurityGroup.objects.get(name=name, organisation=organisation)
        except:
            security_group = SecurityGroup.objects.create(name=name, organisation=organisation, description=description)
            security_group.save()
        return security_group

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_security_group_per_organisation',
                fields=['name', 'organisation'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]
