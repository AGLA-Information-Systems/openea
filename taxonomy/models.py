import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from openea.utils import Utils
from organisation.models import Organisation
from utils.generic import GenericModel

User = get_user_model()

class TagGroup(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_tag_groups')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='tag_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='tag_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='tag_deleted')

    def get_or_create(name, description=''):
        try:
            tag_group = TagGroup.objects.get(name=name)
        except:
            tag_group = TagGroup.objects.create(name=name, description=description)
            tag_group.save()
        return tag_group

    def get_organisation(self):
        return self.organisation
    
    def filter_by_organisation(organisation):
        return TagGroup.objects.filter(organisation=organisation)
     
    def __str__(self):
        return self.name

class Tag(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    tag_group = models.ForeignKey(TagGroup, on_delete=models.CASCADE, null=True, related_name='tag_groups_tags')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='tag_group_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='tag_group_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='tag_group_deleted')

    def get_or_create(name, description=''):
        try:
            tag = Tag.objects.get(name=name)
        except:
            tag = Tag.objects.create(name=name, description=description)
            tag.save()
        return tag

    def get_organisation(self):
        return self.organisation
    
    def filter_by_organisation(organisation):
        return Tag.objects.filter(organisation=organisation)
     
    def __str__(self):
        return self.name
