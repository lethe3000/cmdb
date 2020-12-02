from django.db import models

from apps.main.models.base import PasswordFieldsModel, CreatedModifiedModel


class Credential(PasswordFieldsModel, CreatedModifiedModel):
    PASSWORD_FIELDS = ()
    KIND_CHOICES = (
        ('ssh', 'Machine'),
        ('scm', 'Source Control'),
        ('cloud', 'Cloud'),
        ('kubernetes', 'Kubernetes'),
    )
    kind = models.CharField(
        max_length=32,
        choices=KIND_CHOICES,
        default='ssh',
    )


class Ssh(Credential):
    PASSWORD_FIELDS = ('password', 'private_key', "certificate", "passphrase")

    class Meta:
        proxy = True


class Scm(Credential):
    PASSWORD_FIELDS = ("password", "private_key")

    class Meta:
        proxy = True


class Cloud(Credential):
    PASSWORD_FIELDS = ("password",)

    class Meta:
        proxy = True


class Kubernetes(Credential):
    PASSWORD_FIELDS = ("server_certificate", "client_key", "client_certificate")

    class Meta:
        proxy = True
