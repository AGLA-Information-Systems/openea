import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from openea.utils import Utils
from organisation.models import Organisation, OrganisationManager
from taxonomy.models import Tag, TagGroup
from utils.generic import GenericModel

User = get_user_model()


###############################################################################
### System
###############################################################################
class Repository(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='repositories')
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='repository_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='repository_modified')
    deleted_at = models.DateTimeField(null=True, verbose_name=_("Deleted at"))
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='repository_deleted')

    objects = OrganisationManager()
    
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
     
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Repository')
        verbose_name_plural = _('Repositories')

        constraints = [
            models.UniqueConstraint(
                name='unique_repository_per_organisation',
                fields=['name', 'id', 'organisation'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]

###############################################################################
### Meta
###############################################################################

QUALITY_STATUS_PROPOSED = 'QP'
QUALITY_STATUS_APPROVED = 'QA'
QUALITY_STATUS = [
        (QUALITY_STATUS_PROPOSED, _('Proposed')),
        (QUALITY_STATUS_APPROVED, _('Approved')),
]

class OModel(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=60, blank=True, null=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, null=True, related_name='models')
    tags = models.ManyToManyField(Tag, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_models')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='model_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='model_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='model_deleted')

    objects = OrganisationManager()

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
    
    def get_organisation(self):
        return self.repository.organisation
    
    def filter_by_organisation(organisation):
        return OModel.objects.filter(repository__organisation=organisation)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')

        constraints = [
            models.UniqueConstraint(
                name='unique_model_version_per_repository',
                fields=['name', 'version', 'id', 'repository', 'organisation'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]


class OConcept(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    native = models.BooleanField(default=False)
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='concepts')
    tags = models.ManyToManyField(Tag, blank=True)
    quality_status = models.CharField(max_length=2, choices=QUALITY_STATUS, default=QUALITY_STATUS_PROPOSED)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_concepts')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='concept_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='concept_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='concept_deleted')

    objects = OrganisationManager()

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
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OConcept.objects.filter(model__repository__organisation=organisation)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Concept')
        verbose_name_plural = _('Concepts')

        constraints = [
            models.UniqueConstraint(
                name='unique_concept_per_model',
                fields=['name', 'id', 'model', 'organisation'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]

class ORelation(GenericModel, models.Model):
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
    native = models.BooleanField(default=False)
    type = models.CharField(max_length=4, choices=RELATION_TYPE, default=PROPERTY)
    concept = models.ForeignKey(OConcept, on_delete=models.CASCADE, null=True, related_name='implements')
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='relations')
    tags = models.ManyToManyField(Tag, blank=True)
    quality_status = models.CharField(max_length=2, choices=QUALITY_STATUS, default=QUALITY_STATUS_PROPOSED)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_relations')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='relation_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='relation_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='relation_deleted') 

    objects = OrganisationManager()

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
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return ORelation.objects.filter(model__repository__organisation=organisation)

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')

        constraints = [
            models.UniqueConstraint(
                name='unique_relation_per_model',
                fields=['name', 'id', 'model', 'organisation'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]


class OPredicate(GenericModel, models.Model):
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
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_predicates')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='predicate_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='predicate_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='predicate_deleted')

    objects = OrganisationManager()

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
    def name(self):
        return self.subject.name + ' ' + self.relation.name + ' ' + self.object.name 
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OPredicate.objects.filter(model__repository__organisation=organisation)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Predicate')
        verbose_name_plural = _('Predicates')

        constraints = [
            models.UniqueConstraint(
                name='unique_predicate_per_model',
                fields=['subject', 'relation', 'object', 'id', 'model', 'organisation'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]


class OInstance(GenericModel, models.Model):
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
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_instances')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='instance_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='instance_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='instance_deleted')

    objects = OrganisationManager()

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
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OInstance.objects.filter(model__repository__organisation=organisation)

    def __str__(self):
        return "{} :: {}".format(self.name, self.concept)
    
    class Meta:
        verbose_name = _('Instance')
        verbose_name_plural = _('Instances')

        constraints = [
            models.UniqueConstraint(
                name='unique_instance_per_concept',
                fields=['name', 'id', 'concept', 'model', 'organisation'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]

class OSlot(GenericModel, models.Model):
    """
    Meta class describing predicates between concepts
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=1024, blank=True, null=True)
    value = models.CharField(max_length=1024, blank=True, null=True)
    order = models.CharField(max_length=100, default='0')
    subject = models.ForeignKey(OInstance, on_delete=models.CASCADE, null=True, related_name='slot_subject')
    object = models.ForeignKey(OInstance, on_delete=models.CASCADE, null=True, related_name='slot_object')
    predicate = models.ForeignKey(OPredicate, on_delete=models.CASCADE, null=True, related_name='used_in')
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='slots')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_slots')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='slot_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='slot_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='slot_deleted')

    objects = OrganisationManager()

    # @property
    # def name(self):
    #     if self.name:
    #         name = self.name + ' : '
    #     subject_name = self.value or ''
    #     if self.subject is not None:
    #         subject_name = self.subject.name
    #     object_name = self.value or ''
    #     if self.object is not None:
    #         object_name = self.object.name
    #     name =+ subject_name + ' -> ' + self.predicate.relation.name + ' -> ' + object_name
    #     return name
    
    def get_display(self):
        name = self.name or ""

        if self.subject is None and self.object is not None:
            return name + ' : ' + self.value + ' ' + self.predicate.subject.name 

        if self.subject is not None and self.object is None:
            return name + ' : ' + self.value + ' ' + self.predicate.object.name 
        
        if self.subject is not None and self.object is not None:
            return name + self.subject.name + ' ' + self.predicate.relation.name + ' ' + self.object.name

        raise ValueError('Malformed slot!')

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
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OConcept.objects.filter(model__repository__organisation=organisation)

    def __str__(self):
        return self.get_display()
    
    def __lt__(self, other):
        return True
    
    class Meta:
        verbose_name = _('Slot')
        verbose_name_plural = _('Slots')

        constraints = [
            models.UniqueConstraint(
                name='unique_slot_per_model',
                fields=['subject', 'predicate', 'object', 'model', 'organisation'],
                deferrable=models.Deferrable.DEFERRED,
            )
        ]

class OReport(GenericModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    path = models.CharField(blank=True, null=True, max_length=4096)
    content = models.TextField(blank=True, null=True)
    model = models.ForeignKey(OModel, on_delete=models.CASCADE, null=True, related_name='reports')
    tags = models.ManyToManyField(Tag, blank=True)
    quality_status = models.CharField(max_length=2, choices=QUALITY_STATUS, default=QUALITY_STATUS_PROPOSED)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='organisation_reports')

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, null=True, related_name='report_created')
    modified_at = models.DateTimeField(verbose_name=_("Modified at"), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified by"), on_delete=models.PROTECT, blank=True, null=True, related_name='report_modified')
    deleted_at = models.DateTimeField(verbose_name=_("Deleted at"), blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name=_("Deleted by"), on_delete=models.PROTECT, blank=True, null=True, related_name='report_deleted')

    objects = OrganisationManager()

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
    
    def get_organisation(self):
        return self.model.repository.organisation
    
    def filter_by_organisation(organisation):
        return OConcept.objects.filter(model__repository__organisation=organisation)
    
    @classmethod
    def get_actions(cls):
        return [Utils.PERMISSION_ACTION_CREATE, Utils.PERMISSION_ACTION_LIST, Utils.PERMISSION_ACTION_VIEW, Utils.PERMISSION_ACTION_UPDATE, Utils.PERMISSION_ACTION_EXECUTE]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
