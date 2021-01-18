# Generated by Django 3.1.4 on 2020-12-24 21:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0019_auto_20201222_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emap2secjob',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='emap2secplusjob',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='mainmastjob',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='mainmastsegjob',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='emap2secjob',
            name='time_sub',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Submission Time'),
        ),
        migrations.AddField(
            model_name='emap2secplusjob',
            name='time_sub',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Submission Time'),
        ),
        migrations.AddField(
            model_name='mainmastjob',
            name='time_sub',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Submission Time'),
        ),
        migrations.AddField(
            model_name='mainmastsegjob',
            name='time_sub',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Submission Time'),
        ),
    ]