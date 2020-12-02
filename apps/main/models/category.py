from django.db import models

from apps.main.fields import UidForeignKey
from apps.main.models.base import PrimordialModel, to_uid


class Category(PrimordialModel):
    parent = UidForeignKey(
        'self',
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        related_name='sub_categories',
    )


class App(PrimordialModel):
    git_id = models.PositiveIntegerField(blank=True, null=True)

    category = UidForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='apps'
    )


class Workload(PrimordialModel):
    app = UidForeignKey(
        'App',
        on_delete=models.SET_NULL,
        null=True,
        related_name='workloads'
    )
    category = UidForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='workloads'
    )
    orchestrator = UidForeignKey(
        'Orchestrator',
        on_delete=models.SET_NULL,
        null=True,
        related_name='workloads'
    )
    status = models.CharField(
        max_length=32,
    )


class Env(PrimordialModel):
    pass


class OrchestrationType(PrimordialModel):
    """
    编排类型，例如manual, rancher1.x, helm, jenkins等
    """
    kind = models.CharField(max_length=64)


class Orchestrator(PrimordialModel):
    """
    存储编排信息
    根据type执行相应操作
    """
    type = UidForeignKey(
        'OrchestrationType',
        on_delete=models.SET_NULL,
        null=True,
    )
    env = UidForeignKey(
        'Env',
        on_delete=models.SET_NULL,
        null=True,
        related_name='Orchestrator',
        to_field='uid',
    )
