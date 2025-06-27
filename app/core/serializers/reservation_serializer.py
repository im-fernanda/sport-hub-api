from rest_framework import serializers
from core.models import Category, Reservation, ReservationGuest, TimeSlot, Space
from datetime import datetime
from core.serializers import SpaceSerializer, TimeSlotSerializer, UserSerializer

class ReservationSerializer(serializers.ModelSerializer):
    guests = serializers.SerializerMethodField()
    space = SpaceSerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    space_id = serializers.PrimaryKeyRelatedField(
        queryset=Space.objects.all(), write_only=True, source="space"
    )
    time_slot_id = serializers.PrimaryKeyRelatedField(
        queryset=TimeSlot.objects.all(), write_only=True, source="time_slot"
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "space_id",
            "space",
            "time_slot_id",
            "time_slot",
            "status",
            "guests",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]

    def create(self, validated_data):
        instance = super().create(validated_data)

        guest_names = self.initial_data.get("guests", [])
        for name in guest_names:
            ReservationGuest.objects.create(reservation=instance, guest=name)

        return instance

    def get_guests(self, obj):
        return [g.guest for g in obj.guests.all()]

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.is_admin:
            try:
                category = attrs[
                    "space"
                ].category  
            except Category.DoesNotExist:
                raise serializers.ValidationError("Essa categoria não existe.")

            reservation = Reservation.objects.filter(
                space__category=category,
                user=user,
                created_at__date=datetime.today().date(),
            )

            if reservation.exists():
                raise serializers.ValidationError(
                    "Você já possui uma reserva para essa categoria hoje."
                )
        return attrs
