from django.db import models
from apps.main.models.base import PrimordialModel, to_uid


class Release(PrimordialModel):
    app = to_uid(models.ForeignKey(
        'App',
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        related_name='releases'
    ))

    version = models.CharField(max_length=128)

    due_date = models.DateTimeField(default=None)


class Deployment(PrimordialModel):
    app = to_uid(models.ForeignKey(
        'App',
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        related_name='deployments'
    ))

    release = to_uid(models.ForeignKey(
        'Release',
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        related_name='deployments'
    ))

    workload = to_uid(models.OneToOneField(
        'Workload',
        on_delete=models.SET_NULL,
        default=None,
        null=True,
    ))

    env = to_uid(models.ForeignKey(
        'Env',
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        related_name='deployments'
    ))

    branch = models.CharField(max_length=128, blank=True, null=True, default='')

    pipeline_id = models.PositiveIntegerField(blank=True, null=True)

    params = models.JSONField(default=dict)
