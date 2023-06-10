import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from openea.utils import Utils

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"


###############################################################################
### System
###############################################################################
TASK_TYPE_IMPORT = 'IMPORT'
TASK_TYPE_EXPORT = 'EXPORT'
TASK_TYPE = [
    (TASK_TYPE_IMPORT, 'Import'),
    (TASK_TYPE_EXPORT, 'Export')
]

TASK_STATUS_PENDING = 'PENDING'
TASK_STATUS_STARTED = 'STARTED'
TASK_STATUS_SUCCESS = 'SUCCESS'
TASK_STATUS_WARNING = 'WARNING'
TASK_STATUS_FAILURE = 'FAILURE'
TASK_STATUS_CANCELLED = 'CANCELLED'
TASK_STATUS = [
    (TASK_STATUS_PENDING, 'Pending'),
    (TASK_STATUS_STARTED, 'Started'),
    (TASK_STATUS_SUCCESS, 'Completed successfully'),
    (TASK_STATUS_WARNING, 'Completed with warnings'),
    (TASK_STATUS_FAILURE, 'Failed'),
    (TASK_STATUS_CANCELLED, 'Cancelled')
]
TASK_PROCESSABLE_STATUSES = [TASK_STATUS_PENDING, TASK_STATUS_FAILURE]

class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    location = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    unique_organisation_per_location = models.UniqueConstraint(
        name='unique_organisation_per_location',
        fields=['name', 'location'],
        deferrable=models.Deferrable.DEFERRED,
    )

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.DO_NOTHING, null=True, related_name='organisation_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.DO_NOTHING, null=True, related_name='organisation_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted at"), on_delete=models.DO_NOTHING, null=True, related_name='organisation_deleted')

    def get_or_create(name, description=''):
        try:
            organisation = Organisation.objects.get(name=name)
        except:
            organisation = Organisation.objects.create(name=name, description=description)
            organisation.save()
        return organisation

    def get_object_type():
        return Utils.OBJECT_ORGANISATION

    def get_organisation(self):
        return self
     
    def __str__(self):
        return self.name

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=1024)
    phone = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='profiles')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_profiles')
    is_active = models.BooleanField(default=False)

    # unique_user_profile_per_organisation = models.UniqueConstraint(
    #     name='unique_user_profile_per_organisation',
    #     fields=['user', 'organisation'],
    #     deferrable=models.Deferrable.DEFERRED,
    # )

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.DO_NOTHING, null=True, related_name='profile_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.DO_NOTHING, null=True, related_name='profile_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted at"), on_delete=models.DO_NOTHING, null=True, related_name='profile_deleted')

    @property
    def name(self):
        return self.role

    def get_or_create(organisation, user, role, description=''):
        try:
            profile = Profile.objects.get(organisation=organisation, user=user, role=role)
        except:
            profile = Profile.objects.create(organisation=organisation, user=user, role=role, description=description)
            profile.save()
        return profile

    def get_organisation(self):
        return self.organisation
    
    def filter_by_organisation(organisation):
        return Profile.objects.filter(organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_PROFILE
     
    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='uploads/', null=True)
    type = models.CharField(max_length=10, choices=TASK_TYPE, default='IMPORT')
    status = models.CharField(max_length=10, choices=TASK_STATUS, default='PENDING')
    config = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='tasks')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_tasks')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.DO_NOTHING, null=True, related_name='task_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.DO_NOTHING, null=True, related_name='task_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted at"), on_delete=models.DO_NOTHING, null=True, related_name='task_deleted')

    def get_or_create(name, version=None, description=''):
        try:
            task = Task.objects.get(name=name, version=version)
        except:
            task = Task.objects.create(name=name, version=version, description=description)
            task.save()
        return task

    def get_organisation(self):
        return self.organisation
    
    def filter_by_organisation(organisation):
        return Profile.objects.filter(organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_TASK
     
    def __str__(self):
        return self.name

# TODO: hook log creation
class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=1024)
    target = models.UUIDField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    user = models.UUIDField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING, null=True, related_name='organisation_logs')

    @property
    def name(self):
        return self.source

    def get_organisation(self):
        return self.organisation
    
    def filter_by_organisation(organisation):
        return Profile.objects.filter(organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_LOG
     
    def __str__(self):
        return self.name