from django.db import models

from apps.main.models.base import CreatedModifiedModel


class Profile(CreatedModifiedModel):
    """
    Profile model related to User object. Currently stores LDAP DN for users
    loaded from LDAP.
    """

    class Meta:
        app_label = 'main'

    ldap_dn = models.CharField(
        max_length=1024,
        default='',
    )
