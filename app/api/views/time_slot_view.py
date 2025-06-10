from rest_framework.viewsets import ModelViewSet
from core.serializers import TimeSlotSerializer
from core.models import TimeSlot
from core.permissions import IsTimeSlotAdmin
from rest_framework.permissions import IsAuthenticated

def str_to_bool(value):
    return str(value).lower() in ("true", "1", "yes")


class TimeSlotViewSet(ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated, IsTimeSlotAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        is_available = self.request.query_params.get("is_available")

        if is_available is not None:
            queryset = queryset.filter(is_available=str_to_bool(is_available))

        return queryset
