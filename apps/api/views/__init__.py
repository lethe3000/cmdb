import sys
from collections import OrderedDict

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie


class ApiRootView(APIView):

    permission_classes = (AllowAny,)
    name = 'REST API'
    versioning_class = None
    swagger_topic = 'Versioning'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        """ List supported API versions """
        data = OrderedDict()
        data['description'] = 'APP REST API'
        data['user'] = request.user.username
        return Response(data)


class DjangoMigrationView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        from django.core.management import call_command
        from io import StringIO
        res = StringIO()
        call_command('showmigrations', stdout=res)
        output = res.read()
        return Response('migrations...')


class UidLookupMixin(object):
    lookup_field = 'uid'
