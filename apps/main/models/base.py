from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from crum import get_current_user

from apps.main.utils.common import uid_generator
from apps.main.utils.encryption import encrypt_field, encrypt_value


class BaseModel(models.Model):
    """
    Base model class with common methods for all models.
    """

    class Meta:
        abstract = True

    def __str__(self):
        name = self.name if 'name' in self.__dict__ else self._meta.verbose_name
        pk = self.uid if 'uid' in self.__dict__ else self.pk
        return f'{name}:{pk}'

    def update_fields(self, **kwargs):
        save = kwargs.pop('save', True)
        update_fields = []
        for field, value in kwargs.items():
            if getattr(self, field) != value:
                setattr(self, field, value)
                update_fields.append(field)
        if save and update_fields:
            self.save(update_fields=update_fields)
        return update_fields


class CreatedModifiedModel(BaseModel):
    """
    Common model with created/modified timestamp fields.  Allows explicitly
    specifying created/modified timestamps in certain cases (migrations, job
    events), calculates automatically if not specified.
    """
    class Meta:
        abstract = True

    created = models.DateTimeField(
        default=None,
        editable=False,
    )
    modified = models.DateTimeField(
        default=None,
        editable=False,
    )

    def save(self, *args, **kwargs):
        update_fields = list(kwargs.get('update_fields', []))
        # Manually perform auto_now_add and auto_now logic.
        if not self.pk and not self.created:
            self.created = now()
            if 'created' not in update_fields:
                update_fields.append('created')
        if 'modified' not in update_fields or not self.modified:
            self.modified = now()
            update_fields.append('modified')
        super(CreatedModifiedModel, self).save(*args, **kwargs)


class PasswordFieldsModel(BaseModel):
    """
    Abstract base class for a model with password fields that should be stored
    as encrypted values.
    """

    PASSWORD_FIELDS = ()

    payload = models.JSONField(default=dict)

    class Meta:
        abstract = True

    def save1(self, *args, **kwargs):
        new_instance = not bool(self.pk)
        # If update_fields has been specified, add our field names to it,
        # if it hasn't been specified, then we're just doing a normal save.
        update_fields = kwargs.get('update_fields', [])
        # When first saving to the database, don't store any password field
        # values, but instead save them until after the instance is created.
        # Otherwise, store encrypted values to the database.
        for field in self.PASSWORD_FIELDS:
            if new_instance:
                value = getattr(self, field, '')
                setattr(self, '_saved_%s' % field, value)
                setattr(self, field, '')
            else:
                self.encrypt_field(field)
                self.mark_field_for_save(update_fields, field)
        super().save(*args, **kwargs)
        # After saving a new instance for the first time, set the password
        # fields and save again.
        if new_instance:
            update_fields = []
            for field in self.PASSWORD_FIELDS:
                saved_value = getattr(self, '_saved_%s' % field, '')
                setattr(self, field, saved_value)
                self.mark_field_for_save(update_fields, field)
            self.save(update_fields=update_fields)

    def encrypt_field(self, field):
        encrypted = encrypt_field(self, field)
        setattr(self, field, encrypted)

    def mark_field_for_save(self, update_fields, field):
        if field not in update_fields:
            update_fields.append(field)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class UidFieldMixin(models.Model):
    uid = models.CharField(max_length=64, unique=True, editable=False)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        if not self.pk:
            self.uid = uid_generator(self.__class__.__name__.lower())
            if 'uid' not in update_fields:
                update_fields.append('uid')
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        indexes = [models.Index(fields=['uid'])]


class PrimordialModel(UidFieldMixin, CreatedModifiedModel):
    """
    Common model for all object types that have these standard fields
    must use a subclass CommonModel or CommonModelNameNotUnique though
    as this lacks a name field.
    """

    class Meta:
        abstract = True

    active_objects = ActiveManager()

    name = models.CharField(
        max_length=128,
    )
    display_name = models.CharField(max_length=128, blank=True, null=True, default='')
    description = models.TextField(
        blank=True,
        default='',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%s(class)s_created+',
        default=None,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%s(class)s_modified+',
        default=None,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    owned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%s(class)s_owned+',
        default=None,
        null=True,
        on_delete=models.SET_NULL,
    )
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        user = self.created_by or get_current_user()
        if not self.pk:
            self.created_by = self.owned_by = self.modified_by = user
            for field in ['created_by', 'owned_by', 'modified_by']:
                if field not in update_fields:
                    update_fields.append(field)

        # Update modified_by if any editable fields have changed
        if self.pk and not self.modified_by:
            self.modified_by = user
            if 'modified_by' not in update_fields:
                update_fields.append('modified_by')

        super(PrimordialModel, self).save(*args, **kwargs)

    def clean_description(self):
        # Description should always be empty string, never null.
        return self.description or ''


def to_uid(relation):
    setattr(relation, 'to_field', 'uid')
    return relation
