import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from openea.utils import Utils
from organisation.models import Organisation
from taxonomy.models import Tag, TagGroup

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
class Repository(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='repositories')
    tags = models.ManyToManyField(Tag, blank=True)

    unique_repository_per_organisation = models.UniqueConstraint(
        name='unique_repository_per_organisation',
        fields=['name', 'organisation'],
        deferrable=models.Deferrable.DEFERRED,
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Created at"))
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_("Created by"), related_name='repository_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='repository_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='repository_deleted')

    def get_or_create(name, version=None, description='', id=None):
        try:
            repository = Repository.objects.get(id=id)
        except:
            try:
                repository = Repository.objects.get(name=name)
            except:
                repository = Repository.objects.create(name=name, description=description or '', id=id)
        repository.name = name
        repository.description = description
        repository.save()
        return repository
    
    def get_organisation(self):
        return self.organisation
    
    def filter_by_organisation(organisation):
        return Repository.objects.filter(organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_REPOSITORY
     
    def __str__(self):
        return self.name

###############################################################################
### Meta
###############################################################################

QUALITY_STATUS_PROPOSED = 'QP'
QUALITY_STATUS_APPROVED = 'QA'
QUALITY_STATUS = [
        (QUALITY_STATUS_PROPOSED, _('Proposed')),
        (QUALITY_STATUS_APPROVED, _('Approved')),
]

class OModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=60, blank=True, null=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, null=True, related_name='models')
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='model_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='model_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='model_deleted')

    unique_model_version_per_repository = models.UniqueConstraint(
        name='unique_model_version_per_repository',
        fields=['name', 'version', 'repository'],
        deferrable=models.Deferrable.DEFERRED,
    )

    def get_or_create(name, version=None, description='', repository=None, id=None):
        try:
            model = OModel.objects.get(id=id)
        except:
            try:
                model = OModel.objects.get(repository=repository, name=name, version=version)
            except:
                model = OModel.objects.create(repository=repository, name=name, version=version, description=description or '', id=id)
        model.name = name
        model.version = version
        model.description = description
        model.save()
        return model

    @property
    def organisation(self):
        return self.repository.organisation
    
    def get_organisation(self):
        return self.repository.organisation
    
    def filter_by_organisation(organisation):
        return OModel.objects.filter(repository__organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_MODEL
    
    def __str__(self):
        return self.name


class OConcept(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='concepts')
    tags = models.ManyToManyField(Tag, blank=True)
    quality_status = models.CharField(max_length=2, choices=QUALITY_STATUS, default=QUALITY_STATUS_PROPOSED)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='concept_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='concept_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='concept_deleted')

    def get_or_create(name, description='', model=None, id=None):
        try:
            concept = OConcept.objects.get(model=model,id=id)
        except:
            try:
                concept = OConcept.objects.get(model=model, name=name)
            except:
                concept = OConcept.objects.create(model=model, name=name, description=description or '', id=id)
        concept.name = name
        concept.description = description
        concept.save()
        return concept

    @property
    def organisation(self):
        return self.model.repository.organisation
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OConcept.objects.filter(model__repository__organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_CONCEPT
    
    def __str__(self):
        return self.name

class ORelation(models.Model):
    """
    Meta class describing predicates between concepts
    """
    INHERITANCE_SUPER_IS_SUBJECT = 'HESL'
    INHERITANCE_SUPER_IS_OBJECT = 'HESR'
    PROPERTY = 'PROP'
    RELATION_TYPE = [
        (PROPERTY, _('Property')),
        (INHERITANCE_SUPER_IS_SUBJECT, _('Inheritance (Parent=Subject)')),
        (INHERITANCE_SUPER_IS_OBJECT, _('Inheritance (Parent=Object)')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=4, choices=RELATION_TYPE, default=PROPERTY)
    concept = models.ForeignKey(OConcept, on_delete=models.CASCADE, null=True, related_name='implements')
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='relations')
    tags = models.ManyToManyField(Tag, blank=True)
    quality_status = models.CharField(max_length=2, choices=QUALITY_STATUS, default=QUALITY_STATUS_PROPOSED)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='relation_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='relation_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='relation_deleted')

    unique_relation_per_model = models.UniqueConstraint(
        name='unique_relation_per_model',
        fields=['name', 'model'],
        deferrable=models.Deferrable.DEFERRED,
    )

    def get_or_create(model, name, type=PROPERTY, description='', id=None):
        try:
            relation = ORelation.objects.get(id=id)
        except:
            try:
                relation = ORelation.objects.get(model=model, name=name)
            except:
                relation = ORelation.objects.create(model=model, name=name, type=type, description=description or '', id=id)
        relation.name = name
        relation.description = description
        relation.type = type
        relation.save()
        return relation

    @property
    def organisation(self):
        return self.model.repository.organisation
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return ORelation.objects.filter(model__repository__organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_RELATION

    def __str__(self):
        return "{}".format(self.name)

class OPredicate(models.Model):
    """
    Meta class describing predicates between concepts
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(OConcept, on_delete=models.CASCADE, null=True, related_name='is_subject_of')
    object = models.ForeignKey(OConcept, on_delete=models.CASCADE, null=True, related_name='is_object_of')
    relation = models.ForeignKey(ORelation, on_delete=models.CASCADE, null=True, related_name='used_in')
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='predicates')
    cardinality_min = models.IntegerField(default=0)
    cardinality_max = models.IntegerField(blank=True, null=True, default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    quality_status = models.CharField(max_length=2, choices=QUALITY_STATUS, default=QUALITY_STATUS_PROPOSED)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='predicate_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='predicate_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='predicate_deleted')

    unique_predicate_per_model = models.UniqueConstraint(
        name='unique_predicate_per_model',
        fields=['subject', 'relation', 'object', 'model'],
        deferrable=models.Deferrable.DEFERRED,
    )

    @property
    def name(self):
        return "{} {} {}".format(self.subject.name, self.relation.name, self.object.name)

    def get_or_create(model, relation, description='', subject=None, object=None, cardinality_min = 0, cardinality_max = 0, id=None):
        try:
            predicate = OPredicate.objects.get(id=id)
        except:
            try:
                predicate = OPredicate.objects.get(relation=relation, subject=subject, object=object)
            except:
                predicate = OPredicate.objects.create(model=model, subject=subject, relation=relation, object=object, description=description or '', cardinality_min=cardinality_min, cardinality_max=cardinality_max, id=id)
        predicate.description = description
        predicate.subject = subject
        predicate.object = object
        predicate.relation = relation
        predicate.cardinality_min = cardinality_min
        predicate.cardinality_max= cardinality_max
        predicate.save()
        return predicate

    @property
    def organisation(self):
        return self.model.repository.organisation
    
    @property
    def name(self):
        return self.subject.name + '->' + self.relation.name + '->' + self.object.name 
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OPredicate.objects.filter(model__repository__organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_PREDICATE

    def __str__(self):
        return self.name


class OInstance(models.Model):
    """
    Meta class describing instances between concepts
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    code = models.CharField(max_length=1024, default='')
    description = models.TextField(blank=True, null=True)
    concept = models.ForeignKey(OConcept, on_delete=models.CASCADE, null=True, related_name='instances')
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='model_instances')
    tags = models.ManyToManyField(Tag, blank=True)
    quality_status = models.CharField(max_length=2, choices=QUALITY_STATUS, default=QUALITY_STATUS_PROPOSED)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='instance_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='instance_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='instance_deleted')

    unique_instance_per_model = models.UniqueConstraint(
        name='unique_instance_per_model',
        fields=['name', 'concept'],
        deferrable=models.Deferrable.DEFERRED,
    )

    def get_or_create(model, name, code, concept, description='', id=None):
        try:
            instance = OInstance.objects.get(id=id)
        except:
            try:
                instance = OInstance.objects.get(model=model, name=name, code=code, concept=concept)
            except:
                instance = OInstance.objects.create(model=model, name=name, code=code, concept=concept, description=description or '', id=id)
        instance.description = description
        instance.concept = concept
        instance.save()
        return instance

    @property
    def organisation(self):
        return self.model.repository.organisation
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OInstance.objects.filter(model__repository__organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_INSTANCE

    def __str__(self):
        return "{} :: {}".format(self.name, self.concept)

class OSlot(models.Model):
    """
    Meta class describing predicates between concepts
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=1024, blank=True, null=True)
    order = models.CharField(max_length=100, default='0')
    subject = models.ForeignKey(OInstance, on_delete=models.CASCADE, null=True, related_name='slot_subject')
    object = models.ForeignKey(OInstance, on_delete=models.CASCADE, null=True, related_name='slot_object')
    predicate = models.ForeignKey(OPredicate, on_delete=models.CASCADE, null=True, related_name='used_in')
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='slots')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='slot_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='slot_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='slot_deleted')


    unique_slot_per_model = models.UniqueConstraint(
        name='unique_slot_per_model',
        fields=['subject', 'predicate', 'object', 'model'],
        deferrable=models.Deferrable.DEFERRED,
    )

    @property
    def name(self):
        subject_name = ''
        if self.subject is not None:
            subject_name = self.subject.name
        object_name = self.value
        if self.object is not None:
            object_name = self.object.name
        return subject_name + '->' + self.predicate.relation.name + '->' + object_name 

    def get_or_create(model, predicate, description='', order='0', subject=None, object=None, value=None, id=None):
        try:
            slot = OSlot.objects.get(id=id)
        except:
            try:
                slot = OSlot.objects.get(model=model, predicate=predicate, subject=subject, object=object, value=value)
            except:
                slot = OSlot.objects.create(model=model, predicate=predicate, subject=subject,  object=object, value=value, description=description or '', order=order, id=id)
        slot.description = description
        slot.predicate = predicate
        slot.subject = subject
        slot.object = object
        slot.order = order
        slot.save()
        return slot

    @property
    def organisation(self):
        return self.model.repository.organisation
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OConcept.objects.filter(model__repository__organisation=organisation)

    def get_object_type():
        return Utils.OBJECT_INSTANCE

    def __str__(self):
        return self.name
    
    def __lt__(self, other):
        return True

class OReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    path = models.CharField(blank=True, null=True, max_length=4096)
    content = models.TextField(blank=True, null=True)
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='reports')
    tags = models.ManyToManyField(Tag, blank=True)
    quality_status = models.CharField(max_length=2, choices=QUALITY_STATUS, default=QUALITY_STATUS_PROPOSED)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='report_created')
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='report_modified')
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='report_deleted')

    def get_or_create(name, description='', model=None, id=None, path=None, content=''):
        try:
            report = OReport.objects.get(id=id)
        except:
            try:
                report = OReport.objects.get(model=model, name=name)
            except:
                report = OReport.objects.create(model=model, name=name, description=description or '', path=path, content=content, id=id)
        report.description = description
        report.content = content
        report.path = path
        report.save()
        return report
    
    @property
    def organisation(self):
        return self.model.repository.organisation
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OConcept.objects.filter(model__repository__organisation=organisation)
    
    def get_object_type():
        return Utils.OBJECT_REPORT

    def __str__(self):
        return self.name
