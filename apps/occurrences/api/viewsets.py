from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import OccurrenceSerializer
from ..models import Occurrence


class OccurrenceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                        mixins.CreateModelMixin, mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    """Manage Occurrences in the database"""
    serializer_class = OccurrenceSerializer
    queryset = Occurrence.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the occurrences for the authenticated user"""
        queryset = self.queryset

        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'Message': 'Ocorrência registrada com sucesso', **serializer.data},
                        status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Create a new occurrence"""
        serializer.save(user=self.request.user)
