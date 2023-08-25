# Generated by Django 4.1 on 2023-08-25 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.constraints
import django.db.models.deletion
import utils.generic
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taxonomy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OConcept',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True, null=True)),
                ('quality_status', models.CharField(choices=[('QP', 'Proposed'), ('QA', 'Approved')], default='QP', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='concept_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='concept_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
            ],
            options={
                'verbose_name': 'Concept',
                'verbose_name_plural': 'Concepts',
            },
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='OInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('code', models.CharField(default='', max_length=1024)),
                ('description', models.TextField(blank=True, null=True)),
                ('quality_status', models.CharField(choices=[('QP', 'Proposed'), ('QA', 'Approved')], default='QP', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('concept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='ontology.oconcept')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='instance_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='instance_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
            ],
            options={
                'verbose_name': 'Instance',
                'verbose_name_plural': 'Instances',
            },
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='OModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True, null=True)),
                ('version', models.CharField(blank=True, max_length=60, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='model_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='model_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='model_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_models', to='organisation.organisation')),
            ],
            options={
                'verbose_name': 'Model',
                'verbose_name_plural': 'Models',
            },
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='OPredicate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('cardinality_min', models.IntegerField(default=0)),
                ('cardinality_max', models.IntegerField(blank=True, default=0, null=True)),
                ('quality_status', models.CharField(choices=[('QP', 'Proposed'), ('QA', 'Approved')], default='QP', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='predicate_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='predicate_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='predicates', to='ontology.omodel')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='predicate_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='is_object_of', to='ontology.oconcept')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_predicates', to='organisation.organisation')),
            ],
            options={
                'verbose_name': 'Predicate',
                'verbose_name_plural': 'Predicates',
            },
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(null=True, verbose_name='Deleted at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='repository_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='repository_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='repository_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='organisation.organisation')),
                ('tags', models.ManyToManyField(blank=True, to='taxonomy.tag')),
            ],
            options={
                'verbose_name': 'Repository',
                'verbose_name_plural': 'Repositories',
            },
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='OSlot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('value', models.CharField(blank=True, max_length=1024, null=True)),
                ('order', models.CharField(default='0', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='slot_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='slot_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='ontology.omodel')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='slot_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slot_object', to='ontology.oinstance')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_slots', to='organisation.organisation')),
                ('predicate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='used_in', to='ontology.opredicate')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slot_subject', to='ontology.oinstance')),
            ],
            options={
                'verbose_name': 'Slot',
                'verbose_name_plural': 'Slots',
            },
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='OReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True, null=True)),
                ('path', models.CharField(blank=True, max_length=4096, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('quality_status', models.CharField(choices=[('QP', 'Proposed'), ('QA', 'Approved')], default='QP', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='ontology.omodel')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_reports', to='organisation.organisation')),
                ('tags', models.ManyToManyField(blank=True, to='taxonomy.tag')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='ORelation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('PROP', 'Property'), ('HESL', 'Inheritance (Parent=Subject)'), ('HESR', 'Inheritance (Parent=Object)')], default='PROP', max_length=4)),
                ('quality_status', models.CharField(choices=[('QP', 'Proposed'), ('QA', 'Approved')], default='QP', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('concept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='implements', to='ontology.oconcept')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='relation_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='relation_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relations', to='ontology.omodel')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='relation_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_relations', to='organisation.organisation')),
                ('tags', models.ManyToManyField(blank=True, to='taxonomy.tag')),
            ],
            options={
                'verbose_name': 'Relation',
                'verbose_name_plural': 'Relations',
            },
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.AddField(
            model_name='opredicate',
            name='relation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='used_in', to='ontology.orelation'),
        ),
        migrations.AddField(
            model_name='opredicate',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='is_subject_of', to='ontology.oconcept'),
        ),
        migrations.AddField(
            model_name='opredicate',
            name='tags',
            field=models.ManyToManyField(blank=True, to='taxonomy.tag'),
        ),
        migrations.AddField(
            model_name='omodel',
            name='repository',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='models', to='ontology.repository'),
        ),
        migrations.AddField(
            model_name='omodel',
            name='tags',
            field=models.ManyToManyField(blank=True, to='taxonomy.tag'),
        ),
        migrations.AddField(
            model_name='oinstance',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model_instances', to='ontology.omodel'),
        ),
        migrations.AddField(
            model_name='oinstance',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='instance_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by'),
        ),
        migrations.AddField(
            model_name='oinstance',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_instances', to='organisation.organisation'),
        ),
        migrations.AddField(
            model_name='oinstance',
            name='tags',
            field=models.ManyToManyField(blank=True, to='taxonomy.tag'),
        ),
        migrations.AddField(
            model_name='oconcept',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='concepts', to='ontology.omodel'),
        ),
        migrations.AddField(
            model_name='oconcept',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='concept_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by'),
        ),
        migrations.AddField(
            model_name='oconcept',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_concepts', to='organisation.organisation'),
        ),
        migrations.AddField(
            model_name='oconcept',
            name='tags',
            field=models.ManyToManyField(blank=True, to='taxonomy.tag'),
        ),
        migrations.AddConstraint(
            model_name='repository',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('name', 'id', 'organisation'), name='unique_repository_per_organisation'),
        ),
        migrations.AddConstraint(
            model_name='oslot',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('subject', 'predicate', 'object', 'model', 'organisation'), name='unique_slot_per_model'),
        ),
        migrations.AddConstraint(
            model_name='orelation',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('name', 'id', 'model', 'organisation'), name='unique_relation_per_model'),
        ),
        migrations.AddConstraint(
            model_name='opredicate',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('subject', 'relation', 'object', 'id', 'model', 'organisation'), name='unique_predicate_per_model'),
        ),
        migrations.AddConstraint(
            model_name='omodel',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('name', 'version', 'id', 'repository', 'organisation'), name='unique_model_version_per_repository'),
        ),
        migrations.AddConstraint(
            model_name='oinstance',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('name', 'id', 'concept', 'model', 'organisation'), name='unique_instance_per_concept'),
        ),
        migrations.AddConstraint(
            model_name='oconcept',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('name', 'id', 'model', 'organisation'), name='unique_concept_per_model'),
        ),
    ]
