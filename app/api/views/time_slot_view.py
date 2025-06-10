from rest_framework.viewsets import ModelViewSet
from core.serializers import TimeSlotSerializer
from core.models import TimeSlot
from core.permissions import IsTimeSlotAdmin
from rest_framework.permissions import IsAuthenticated

from datetime import datetime


def str_to_bool(value):
    return str(value).lower() in ("true", "1", "yes")


class TimeSlotViewSet(ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated, IsTimeSlotAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get("date")
        is_available = self.request.query_params.get("is_available")

        if is_available is not None:
            queryset = queryset.filter(is_available=str_to_bool(is_available))

        if date is not None:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                queryset = queryset.filter(date=parsed_date)
            except ValueError:
                raise ValidationError(
                    {"date": "Formato de data inválido. Use YYYY-MM-DD."}
                )
        return queryset
