# Generated by Django 4.1 on 2022-11-16 20:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.JSONField(blank=True, null=True)),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_configurations', to='webapp.organisation')),
            ],
        ),
    ]
