from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response

from apps.api.serializers import CategorySerializer, AppSerializer, EnvSerializer, CategorySimpleSerializer
from apps.api.views import UidLookupMixin
from apps.main.models import Category, App, Env


class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.active_objects.select_related('owned_by', 'created_by', 'modified_by').all()


class CategoryDetail(UidLookupMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.active_objects.all()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryChildren(ListAPIView):
    serializer_class = CategorySimpleSerializer
    queryset = Category.active_objects.select_related('owned_by', 'created_by', 'modified_by').all()

    def get_queryset(self):
        return Category.active_objects.select_related('owned_by', 'created_by', 'modified_by').\
            filter(parent__uid=self.request.query_params.get('uid'))


class AppList(ListCreateAPIView):
    serializer_class = AppSerializer
    queryset = App.active_objects.all()


class AppDetail(UidLookupMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = AppSerializer
    queryset = Category.active_objects.all()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class EnvList(ListCreateAPIView):
    serializer_class = EnvSerializer
    queryset = Env.active_objects.all()


class EnvDetail(UidLookupMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = EnvSerializer
    queryset = Env.active_objects.all()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)
