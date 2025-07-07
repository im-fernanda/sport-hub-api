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

        time_slot = instance.time_slot
        time_slot.is_available = False
        time_slot.save()
        return instance
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Atualiza o time_slot para disponível antes de deletar a reserva
        time_slot = instance.time_slot
        time_slot.is_available = True
        time_slot.save()

        # Deleta a reserva
        self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_guests(self, obj):
        return [g.guest for g in obj.guests.all()]

    def validate(self, attrs):
        user = self.context["request"].user
        space = attrs.get("space")
        time_slot = attrs.get("time_slot")

        if not space or not time_slot:
            raise serializers.ValidationError("Espaço e horário devem ser informados.")

        category = space.category
        reservation_date = time_slot.date  
        # Consulta reservas existentes do mesmo usuário, mesma categoria e mesma data
        existing_reservations = Reservation.objects.filter(
            user=user,
            space__category=category,
            time_slot__date=reservation_date,
        )

        if self.instance:
            existing_reservations = existing_reservations.exclude(pk=self.instance.pk)

        if existing_reservations.exists():
            raise serializers.ValidationError(
                "Você já possui uma reserva para essa categoria nesta data."
            )

        return attrs
