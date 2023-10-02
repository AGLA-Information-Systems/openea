import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from log.middleware.request import get_request
from openea.utils import Utils
from utils.generic import GenericModel

User = get_user_model()


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


# class DeleteManager(models.Manager):
#     def get_queryset(self):
#         request = get_request()
#         if request and request.user and request.user.is_authenticated:
#             #if request.user.is_superuser:
#             #    return super().get_queryset()
#             return super().get_queryset().filter(deleted_at__isnull=True)
#         return super().get_queryset()
    
#     # def delete(self):
#     #     self.delete()

#     def create(self, **obj_data):
#         obj_data['deleted_at'] = None
#         obj_data['deleted_by'] = None
#         return super().create(**obj_data) # Python 3 syntax!!

class OrganisationManager(models.Manager):
    def get_queryset(self):
        request = get_request()
        if request and request.user and request.user.is_authenticated:
            if request.user.organisation and not request.user.is_superuser:
                return super().get_queryset().filter(organisation_id__in=[request.user.organisation.id])
        return super().get_queryset()


class Organisation(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    location = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='organisation_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='organisation_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='organisation_deleted')

    def get_or_create(name, description=''):
        try:
            organisation = Organisation.objects.get(name=name)
        except:
            organisation = Organisation.objects.create(name=name, description=description)
            organisation.save()
        return organisation
    
    @classmethod
    def get_actions(cls, superadmin=False):
        if superadmin:
            return [Utils.PERMISSION_ACTION_CREATE, Utils.PERMISSION_ACTION_LIST, Utils.PERMISSION_ACTION_VIEW, Utils.PERMISSION_ACTION_UPDATE, Utils.PERMISSION_ACTION_DELETE]
        return [Utils.PERMISSION_ACTION_CREATE, Utils.PERMISSION_ACTION_LIST, Utils.PERMISSION_ACTION_VIEW, Utils.PERMISSION_ACTION_UPDATE]

    def get_organisation(self):
        return self
     
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_organisation_per_location',
                fields=['name', 'location'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]

class Profile(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=1024)
    phone = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='profiles')
    is_active = models.BooleanField(default=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_profiles')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='profile_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='profile_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='profile_deleted')

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
     
    def __str__(self):
        return self.name


class Task(GenericModel, models.Model):
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
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='tasks')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_tasks')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='task_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='task_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='task_deleted')

    objects = OrganisationManager()

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
     
    def __str__(self):
        return self.name
