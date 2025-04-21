from rest_framework.viewsets import ModelViewSet
from core.serializers import SpaceSerializer
from core.models import Space
from core.permissions import IsSpaceAdmin

from rest_framework.permissions import IsAuthenticated

class SpaceViewSet(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated, IsSpaceAdmin]