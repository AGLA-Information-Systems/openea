# Generated by Django 4.1 on 2022-11-22 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0002_configuration_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='name',
            field=models.CharField(max_length=1024),
        ),
    ]
