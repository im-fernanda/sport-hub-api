from rest_framework.viewsets import ModelViewSet
from core.serializers import ReservationSerializer
from core.models import Reservation
from core.permissions import IsReservationSelf

from rest_framework.permissions import IsAuthenticated


class ReservationViewSet(ModelViewSet):
    """
    A viewset for viewing and editing reservation instances.
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsReservationSelf]

    def get_queryset(self):
        """
        Optionally restricts the returned reservations to a given user,
        by filtering against a `user` query parameter in the URL.
        """
        if self.request.user.is_admin:
            return self.queryset

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the user as the current user when creating a reservation.
        """
        serializer.save(user=self.request.user)
