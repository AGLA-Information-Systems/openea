import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from openea.utils import Utils
from organisation.models import Organisation, Profile


class SecurityGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    profiles = models.ManyToManyField(Profile, related_name='security_groups')
    organisation = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING, null=True, related_name='organisation_security_groups')

    unique_security_group_per_organisation = models.UniqueConstraint(
        name='unique_security_group_per_organisation',
        fields=['name', 'organisation'],
        deferrable=models.Deferrable.DEFERRED,
    )

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.DO_NOTHING, null=True, related_name='security_group_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.DO_NOTHING, null=True, related_name='security_group_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted at"), on_delete=models.DO_NOTHING, null=True, related_name='security_group_deleted')

    def get_or_create(name, organisation, description=''):
        try:
            security_group = SecurityGroup.objects.get(name=name, organisation=organisation)
        except:
            security_group = SecurityGroup.objects.create(name=name, organisation=organisation, description=description)
            security_group.save()
        return security_group
    
    def get_object_type():
        return Utils.OBJECT_SECURITY_GROUP

    def __str__(self):
        return self.name


class Permission(models.Model):
    PERMISSION_OBJECT_TYPE = Utils.ROOT_OBJECT_TYPE + Utils.DEFAULT_OBJECT_TYPE

    PERMISSION_ACTION_LIST = 'LIST'
    PERMISSION_ACTION_CREATE = 'CREATE'
    PERMISSION_ACTION_VIEW = 'VIEW'
    PERMISSION_ACTION_UPDATE = 'UPDATE'
    PERMISSION_ACTION_DELETE = 'DELETE'
    PERMISSION_ACTION_RUN = 'RUN'
    PERMISSION_ACTION_EXPORT = 'EXPORT'
    PERMISSION_ACTION_IMPORT = 'IMPORT'
    PERMISSION_ACTION = [
        (PERMISSION_ACTION_LIST, 'List'),
        (PERMISSION_ACTION_CREATE, 'Create'),
        (PERMISSION_ACTION_VIEW, 'View'),
        (PERMISSION_ACTION_UPDATE, 'Update'),
        (PERMISSION_ACTION_DELETE, 'Delete'),
        (PERMISSION_ACTION_RUN, 'Run'),
        (PERMISSION_ACTION_IMPORT, 'Import'),
        (PERMISSION_ACTION_EXPORT, 'Export')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=6, choices=PERMISSION_ACTION, default=PERMISSION_ACTION_VIEW)
    description = models.TextField(blank=True, null=True)
    security_groups = models.ManyToManyField(SecurityGroup, related_name='permissions')
    object_type = models.CharField(max_length=4, choices=PERMISSION_OBJECT_TYPE)
    object_identifier = models.UUIDField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING, null=True, related_name='organisation_permissions')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.DO_NOTHING, null=True, related_name='permission_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.DO_NOTHING, null=True, related_name='permission_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted at"), on_delete=models.DO_NOTHING, null=True, related_name='permission_deleted')

    unique_permission_per_organisation = models.UniqueConstraint(
        name='unique_permission_per_organisation',
        fields=['action', 'object_type', 'object_identifier', 'organisation'],
        deferrable=models.Deferrable.DEFERRED,
    )

    def get_or_create(action, object_type, organisation, object_identifier=None, description=''):
        try:
            permission = Permission.objects.get(action=action, object_type=object_type, organisation=organisation, object_identifier=object_identifier)
        except:
            permission = Permission.objects.create(action=action, object_type=object_type, organisation=organisation, object_identifier=object_identifier, description=description)
            permission.save()
        return permission

    def get_object_type():
        return Utils.OBJECT_PERMISSION
     
    def __str__(self):
        return "{}:{}:{}".format(self.organisation, self.action, self.object_type)
