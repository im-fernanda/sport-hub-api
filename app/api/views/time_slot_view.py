from rest_framework.viewsets import ModelViewSet
from core.serializers import TimeSlotSerializer
from core.models import TimeSlot
from core.permissions import IsTimeSlotAdmin
from rest_framework.permissions import IsAuthenticated


class TimeSlotViewSet(ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated, IsTimeSlotAdmin]
