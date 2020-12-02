from rest_framework import status
from rest_framework.response import Response

from apps.api.serializers import ReleaseSerializer, DeploymentSerializer
from apps.main.models import Release, Deployment

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ReleaseList(ListCreateAPIView):
    serializer_class = ReleaseSerializer
    queryset = Release.active_objects.all()


class ReleaseDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ReleaseSerializer
    queryset = Release.active_objects.all()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeploymentList(ListCreateAPIView):
    serializer_class = DeploymentSerializer
    queryset = Deployment.active_objects.all()
