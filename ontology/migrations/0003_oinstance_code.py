# Generated by Django 4.1 on 2022-11-23 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontology', '0002_remove_oconcept_tag_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='oinstance',
            name='code',
            field=models.CharField(default='', max_length=1024),
        ),
    ]
