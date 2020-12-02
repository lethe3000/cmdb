import copy
import logging
from typing import Dict

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import ManyRelatedField

from apps.main.models import Release, Deployment
from apps.main.models.category import Category, App, Env

logger = logging.getLogger('apps.api.serializer')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'date_joined', 'is_active',]


class BaseSerializerMetaclass(serializers.SerializerMetaclass):
    '''
    Custom metaclass to enable attribute inheritance from Meta objects on
    serializer base classes.

    Also allows for inheriting or updating field lists from base class(es):

        class Meta:

            # Inherit all fields from base class.
            fields = ('*',)

            # Inherit all fields from base class and add 'foo'.
            fields = ('*', 'foo')

            # Inherit all fields from base class except 'bar'.
            fields = ('*', '-bar')

            # Define fields as 'foo' and 'bar'; ignore base class fields.
            fields = ('foo', 'bar')

            # Extra field kwargs dicts are also merged from base classes.
            extra_kwargs = {
                'foo': {'required': True},
                'bar': {'read_only': True},
            }

            # If a subclass were to define extra_kwargs as:
            extra_kwargs = {
                'foo': {'required': False, 'default': ''},
                'bar': {'label': 'New Label for Bar'},
            }

            # The resulting value of extra_kwargs would be:
            extra_kwargs = {
                'foo': {'required': False, 'default': ''},
                'bar': {'read_only': True, 'label': 'New Label for Bar'},
            }

            # Extra field kwargs cannot be removed in subclasses, only replaced.

    '''

    @staticmethod
    def _is_list_of_strings(x):
        return isinstance(x, (list, tuple)) and all([isinstance(y, str) for y in x])

    @staticmethod
    def _is_extra_kwargs(x):
        return isinstance(x, dict) and all([isinstance(k, str) and isinstance(v, dict) for k,v in x.items()])

    @classmethod
    def _update_meta(cls, base, meta, other=None):
        for attr in dir(other):
            if attr.startswith('_'):
                continue
            val = getattr(other, attr)
            meta_val = getattr(meta, attr, None)
            # Special handling for lists/tuples of strings (field names).
            if cls._is_list_of_strings(val) and cls._is_list_of_strings(meta_val or []):
                meta_val = meta_val or []
                new_vals = []
                except_vals = []
                if base: # Merge values from all bases.
                    new_vals.extend([x for x in meta_val])
                for v in val:
                    if not base and v == '*': # Inherit all values from previous base(es).
                        new_vals.extend([x for x in meta_val])
                    elif not base and v.startswith('-'): # Except these values.
                        except_vals.append(v[1:])
                    else:
                        new_vals.append(v)
                val = []
                for v in new_vals:
                    if v not in except_vals and v not in val:
                        val.append(v)
                val = tuple(val)
            # Merge extra_kwargs dicts from base classes.
            elif cls._is_extra_kwargs(val) and cls._is_extra_kwargs(meta_val or {}):
                meta_val = meta_val or {}
                new_val = {}
                if base:
                    for k,v in meta_val.items():
                        new_val[k] = copy.deepcopy(v)
                for k,v in val.items():
                    new_val.setdefault(k, {}).update(copy.deepcopy(v))
                val = new_val
            # Any other values are copied in case they are mutable objects.
            else:
                val = copy.deepcopy(val)
            setattr(meta, attr, val)

    def __new__(cls, name, bases, attrs):
        meta = type('Meta', (object,), {})
        for base in bases[::-1]:
            cls._update_meta(base, meta, getattr(base, 'Meta', None))
        cls._update_meta(None, meta, attrs.get('Meta', meta))
        attrs['Meta'] = meta
        return super(BaseSerializerMetaclass, cls).__new__(cls, name, bases, attrs)


class BaseSerializer(serializers.ModelSerializer, metaclass=BaseSerializerMetaclass):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    owned_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    modified_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(BaseSerializer, self).__init__(*args, **kwargs)
        # The following lines fix the problem of being able to pass JSON dict into PrimaryKeyRelatedField.
        data = kwargs.get('data', False)
        if data:
            for field_name, field_instance in self.fields.items():
                if isinstance(field_instance, ManyRelatedField) and not field_instance.read_only:
                    if isinstance(data.get(field_name, False), dict):
                        raise serializers.ValidationError('Cannot use dictionary for %s' % field_name)

    def to_representation(self, instance) -> Dict:
        rep = super().to_representation(instance)
        rep['created_by'] = UserSerializer(instance.created_by).data
        rep['owned_by'] = UserSerializer(instance.owned_by).data
        rep['modified_by'] = UserSerializer(instance.modified_by).data
        return rep

    class Meta:
        fields = ('name', 'display_name', 'description', 'created', 'modified',
                  'created_by', 'owned_by', 'modified_by')


class CreatedOwnedMixin(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    owned_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    modified_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    def to_representation(self, instance) -> Dict:
        rep = super().to_representation(instance)
        # rep.pop('id')
        rep['created_by'] = UserSerializer(instance.created_by).data
        rep['owned_by'] = UserSerializer(instance.owned_by).data
        rep['modified_by'] = UserSerializer(instance.modified_by).data
        return rep


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ('*', 'parent')


class CategorySimpleSerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ('*', '-created_by', '-owned_by', '-modified_by', '-created', '-modified')


class AppSerializer(BaseSerializer):
    class Meta:
        model = App
        fields = ('*', 'git_id', 'category')


class EnvSerializer(BaseSerializer):
    class Meta:
        model = Env


class ReleaseSerializer(BaseSerializer):
    class Meta:
        model = Release
        fields = ('*', 'app', 'version', 'due_date')


class DeploymentSerializer(CreatedOwnedMixin):
    def create(self, validated_data):
        deployment: Deployment = super().create(validated_data)
        return deployment

    class Meta:
        model = Deployment
        fields = ('*', 'app', 'release', 'workload', 'env', 'branch', 'pipeline_id', 'params')
