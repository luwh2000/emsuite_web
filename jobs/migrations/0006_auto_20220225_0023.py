# Generated by Django 3.1.6 on 2022-02-25 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20220224_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emap2secplusjob',
            name='map_file',
            field=models.FileField(null=True, upload_to='emap2secplus', verbose_name='Map File'),
        ),
    ]
