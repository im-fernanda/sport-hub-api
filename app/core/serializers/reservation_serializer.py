from rest_framework import serializers
from core.models import Category, Reservation, ReservationGuest
from datetime import datetime


class ReservationSerializer(serializers.ModelSerializer):
    guests = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "time_slot",
            "space",
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
                category = Category.objects.get(id=attrs["space"].category.id)
            except Category.DoesNotExist:
                raise serializers.ValidationError("Category does not exist.")

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
