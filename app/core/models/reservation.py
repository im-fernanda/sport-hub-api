from django.db import models


class Reservation(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="reservations"
    )
    time_slot = models.ForeignKey(
        "TimeSlot", on_delete=models.CASCADE, related_name="reservations"
    )
    space = models.ForeignKey(
        "Space", on_delete=models.CASCADE, related_name="reservations"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("confirmada", "Confirmada"),
            ("cancelada", "Cancelada"),
            ("concluída", "Concluída"),
        ],
        default="confirmada",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["space", "time_slot"],
                name="unique_space_time_slot",
                violation_error_message="Este espaço já está reservado neste horário.",
            )
        ]

    def __str__(self):
        return f"Reservation by {self.user} for {self.space} on {self.date} at {self.time_slot}"


class ReservationGuest(models.Model):
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="guests"
    )
    guest = models.CharField(max_length=500)

    def __str__(self):
        return f"Guest {self.guest} for reservation {self.reservation}"
