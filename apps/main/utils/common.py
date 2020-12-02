import re
import string
import random

from rest_framework.exceptions import ParseError


def get_object_or_400(klass, *args, **kwargs):
    '''
    Return a single object from the given model or queryset based on the query
    params, otherwise raise an exception that will return in a 400 response.
    '''
    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist as e:
        raise ParseError(*e.args)
    except queryset.model.MultipleObjectsReturned as e:
        raise ParseError(*e.args)


def to_python_boolean(value, allow_none=False):
    value = str(value)
    if value.lower() in ('true', '1', 't'):
        return True
    elif value.lower() in ('false', '0', 'f'):
        return False
    elif allow_none and value.lower() in ('none', 'null'):
        return None
    else:
        raise ValueError(_(u'Unable to convert "%s" to boolean') % value)


def region_sorting(region):
    # python3's removal of sorted(cmp=...) is _stupid_
    if region[1].lower() == 'all':
        return ''
    elif region[1].lower().startswith('us'):
        return region[1]
    return 'ZZZ' + str(region[1])


def camelcase_to_underscore(s: str) -> str:
    '''
    Convert CamelCase names to lowercase_with_underscore.
    '''
    s = re.sub(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s)
    return s.lower().strip('_')


def underscore_to_camelcase(s: str) -> str:
    '''
    Convert lowercase_with_underscore names to CamelCase.
    '''
    return ''.join(x.capitalize() or '_' for x in s.split('_'))


def uid_generator(ins: str, size=5, chars=string.ascii_lowercase + string.digits) -> str:
    return f'{ins}-{"".join(random.choice(chars) for _ in range(size))}'
