from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


STATUSES = (
    (0, 'Queued'),
    (1, 'Running'),
    (2, 'Completed'),
    (3, 'Failed'),
)

# Create your models here.


class Emap2SecJob(models.Model):

    NORMS = (
        (0, 'None'),
        (1, 'Global'),
        (2, 'Local'),
    )

    class Meta:
        verbose_name = 'Emap2Sec Job'
        verbose_name_plural = 'Emap2Sec Jobs'
        db_table = 'emap2sec'

    id = models.UUIDField('UUID', primary_key=True, default=uuid.uuid4)
    name = models.CharField('Job Name', max_length=300, default='')
    comment = models.TextField('Comment', default='', blank=True)
    time_sub = models.DateTimeField('Submission Time', default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    mrc_file = models.FileField('MRC File', upload_to='emap2sec', null=True)
    mrc_filename = models.CharField('MRC Filename', max_length=260, default='')
    contour = models.FloatField('Contour Level', default=0.0)
    sstep = models.PositiveSmallIntegerField('Stride Step', default=2)
    vw = models.PositiveSmallIntegerField('Sliding Cube Size', default=5)
    norm = models.PositiveSmallIntegerField(
        'Density Normalization', choices=NORMS, default=1)


class Emap2SecPlusJob(models.Model):

    class Meta:
        verbose_name = 'Emap2Sec+ Job'
        verbose_name_plural = 'Emap2Sec+ Jobs'
        db_table = 'emap2sec_plus'

    id = models.UUIDField('UUID', primary_key=True, default=uuid.uuid4)
    time_sub = models.DateTimeField('Submission Time', default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    mrc_file = models.FileField(
        'MRC File', upload_to='emap2secplus', null=True)
    mrc_filename = models.CharField('MRC Filename', max_length=260, default='')


class MainmastJob(models.Model):

    class Meta:
        verbose_name = 'MAINMAST Job'
        verbose_name_plural = 'MAINMAST Jobs'
        db_table = 'mainmast'

    id = models.UUIDField('UUID', primary_key=True, default=uuid.uuid4)
    time_sub = models.DateTimeField('Submission Time', default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    mrc_file = models.FileField('MRC File', upload_to='mainmast', null=True)
    mrc_filename = models.CharField('MRC Filename', max_length=260, default='')


class MainmastSegJob(models.Model):

    class Meta:
        verbose_name = 'MAINMASTseg Job'
        verbose_name_plural = 'MAINMASTseg Jobs'
        db_table = 'mainmast_seg'

    id = models.UUIDField('UUID', primary_key=True, default=uuid.uuid4)
    time_sub = models.DateTimeField('Submission Time', default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    mrc_file = models.FileField('MRC File', upload_to='mainmastseg', null=True)
    mrc_filename = models.CharField('MRC Filename', max_length=260, default='')
