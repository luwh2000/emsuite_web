from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


STATUSES = (
    (0, 'Initializing'),
    (1, 'Queued'),
    (2, 'Running'),
    (3, 'Completed'),
    (4, 'Failed'),
)

# Create your models here.


class Emap2SecJob(models.Model):

    NORMS = (
        (0, 'Global'),
        (1, 'Local'),
    )

    class Meta:
        verbose_name = 'Emap2Sec Job'
        verbose_name_plural = 'Emap2Sec Jobs'
        db_table = 'emap2sec'

    id = models.UUIDField('UUID', default=uuid.uuid4, primary_key=True)
    name = models.CharField('Job Name', max_length=300, default='')
    comment = models.TextField('Comment', default='', blank=True)
    time_sub = models.DateTimeField('Submission Time', default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    map_file = models.FileField(
        'Map File', upload_to='emap2sec/input', null=True)
    solved_structure = models.FileField(
        'Solved Crystal Structure', upload_to='emap2sec/solved', null=True, blank=True)
    map_filename = models.CharField('Map Filename', max_length=260, default='')
    contour = models.FloatField('Contour Level', default=0.0)
    sstep = models.PositiveSmallIntegerField('Stride Step', default=2)
    vw = models.PositiveSmallIntegerField('Sliding Cube Size', default=5)
    norm = models.PositiveSmallIntegerField(
        'Density Normalization', choices=NORMS, default=1)


class Emap2SecPlusJob(models.Model):

    TYPES = (
        (0, 'Simulated (6 Å)'),
        (1, 'Simulated (6-10 Å)'),
        (2, 'Simulated (10 Å)'),
        (3, 'Experimental')
    )

    class Meta:
        verbose_name = 'Emap2Sec+ Job'
        verbose_name_plural = 'Emap2Sec+ Jobs'
        db_table = 'emap2sec_plus'

    id = models.UUIDField('UUID', default=uuid.uuid4, primary_key=True)
    time_sub = models.DateTimeField('Submission Time', default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    map_file = models.FileField(
        'Map File', upload_to='emap2secplus\input', null=True)
    map_filename = models.CharField('Map Filename', max_length=260, default='')
    name = models.CharField('Job Name', max_length=300, default='')
    contour = models.FloatField('Contour Level', default=0.0)
    comment = models.TextField('Comment', default='', blank=True)
    type = models.PositiveSmallIntegerField('Map Type', choices=TYPES, default=1)
    resize = models.BooleanField('Resize', default=True)


class MainmastJob(models.Model):

    class Meta:
        verbose_name = 'MAINMAST Job'
        verbose_name_plural = 'MAINMAST Jobs'
        db_table = 'mainmast'

    id = models.UUIDField('UUID', default=uuid.uuid4, primary_key=True)
    name = models.CharField('Job Name', max_length=300, default='')
    comment = models.TextField('Comment', default='', blank=True)
    time_sub = models.DateTimeField('Submission Time', default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    map_file = models.FileField('Map File', upload_to='mainmast', null=True)
    map_filename = models.CharField('Map Filename', max_length=260, default='')
    gw = models.FloatField('Gaussian Kernel Bandwidth', default=2.0)
    Dkeep = models.FloatField('Edge Length Threshold', default=0.5)
    t = models.FloatField('Grid Point Density Threshold', default=0.0)
    allow = models.FloatField('Maximum Shift Distance', default=10.0)
    filter = models.FloatField('Seed Point Density Threshold', default=0.1)
    merge = models.FloatField('Merge Threshold', default=0.5)
    Nround = models.PositiveIntegerField('Number of Iterations', default=5000)
    Nnb = models.PositiveIntegerField('Candidates per Iteration', default=30)
    Ntb = models.PositiveIntegerField('Tabu List Size', default=100)
    Rlocal = models.FloatField('Local MST Radius', default=10.0)
    Const = models.FloatField('Tree Length Constraint', default=1.01)


class MainmastSegJob(models.Model):

    class Meta:
        verbose_name = 'MAINMASTseg Job'
        verbose_name_plural = 'MAINMASTseg Jobs'
        db_table = 'mainmast_seg'

    id = models.UUIDField('UUID', default=uuid.uuid4, primary_key=True)
    time_sub = models.DateTimeField('Submission Time', default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    map_file = models.FileField('Map File', upload_to='mainmastseg', null=True)
    map_filename = models.CharField('Map Filename', max_length=260, default='')
