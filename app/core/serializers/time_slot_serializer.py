from rest_framework import serializers
from core.models import TimeSlot
from datetime import datetime, timedelta


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = [
            "id",
            "date",
            "start_time",
            "end_time",
            "is_holiday",
            "is_available"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "is_holiday": {"required": False},
            "is_avaliable": {"required": False},
        }

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if start_time >= end_time:
            raise serializers.ValidationError("Horário de início deve ser antes do hora de fim.")

        start_timedelta = timedelta(hours=start_time.hour, minutes=start_time.minute)
        end_timedelta = timedelta(hours=end_time.hour, minutes=end_time.minute)

        if end_timedelta - start_timedelta > timedelta(hours=1):
            raise serializers.ValidationError("Time slot não pode exceder 1 hora.")

        return super().validate(attrs)
