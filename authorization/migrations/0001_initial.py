# Generated by Django 4.1 on 2023-08-25 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.constraints
import django.db.models.deletion
import utils.generic
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPermission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('object_identifier', models.UUIDField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accesspermission_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accesspermission_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accesspermission_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_accesspermissions', to='organisation.organisation')),
            ],
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='SecurityGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('accesspermissions', models.ManyToManyField(related_name='security_group_accesspermissions', to='authorization.accesspermission')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='security_group_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='security_group_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='security_group_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_security_groups', to='organisation.organisation')),
                ('profiles', models.ManyToManyField(related_name='security_groups', to='organisation.profile')),
            ],
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('LIST', 'List'), ('CREATE', 'Create'), ('VIEW', 'View'), ('UPDATE', 'Update'), ('DELETE', 'Delete'), ('EXECUTE', 'Execute')], default='VIEW', max_length=10)),
                ('object_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='permission_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='permission_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='permission_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            bases=(utils.generic.GenericModel, models.Model),
        ),
        migrations.AddField(
            model_name='accesspermission',
            name='permission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permission_accesspermissions', to='authorization.permission'),
        ),
        migrations.AddConstraint(
            model_name='securitygroup',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('name', 'organisation'), name='unique_security_group_per_organisation'),
        ),
        migrations.AddConstraint(
            model_name='permission',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('action', 'object_type'), name='unique_permission_per_system'),
        ),
    ]
