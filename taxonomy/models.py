import uuid
from django.db import models
from django.contrib.auth.models import User
from openea.utils import Utils
from webapp.models import Organisation

class TagGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING, null=True, related_name='organisation_tag_groups')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tag_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tag_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tag_deleted')

    def get_or_create(name, description=''):
        try:
            tag_group = TagGroup.objects.get(name=name)
        except:
            tag_group = TagGroup.objects.create(name=name, description=description)
            tag_group.save()
        return tag_group

    def get_organisation(self):
        return self.organisation

    def get_object_type():
        return Utils.OBJECT_TAG_GROUP
     
    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    tag_group = models.ForeignKey(TagGroup, on_delete=models.DO_NOTHING, null=True, related_name='tag_groups_tags')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tag_group_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tag_group_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tag_group_deleted')

    def get_or_create(name, description=''):
        try:
            tag = Tag.objects.get(name=name)
        except:
            tag = Tag.objects.create(name=name, description=description)
            tag.save()
        return tag

    def get_organisation(self):
        return self.organisation

    def get_object_type():
        return Utils.OBJECT_TAG
     
    def __str__(self):
        return self.name
