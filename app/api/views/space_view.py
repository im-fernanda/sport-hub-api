from rest_framework.viewsets import ModelViewSet
from core.serializers import SpaceSerializer
from core.models import Space
from core.permissions import IsSpaceAdmin
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated


class SpaceViewSet(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated, IsSpaceAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]  # Permite filtragem por ID da categoria
