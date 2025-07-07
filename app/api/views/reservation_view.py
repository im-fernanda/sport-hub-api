from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from core.serializers import ReservationSerializer
from core.models import Reservation
from core.permissions import IsReservationSelf


class ReservationViewSet(ModelViewSet):
    """
    A viewset for viewing and editing reservation instances.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsReservationSelf]

    def get_queryset(self):
        """
        Retorna todas as reservas se o usuário for admin.
        Caso contrário, retorna apenas as reservas feitas por ele mesmo.
        """
        if self.request.user.is_admin:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="minhas-reservas")
    def minhas_reservas(self, request):
        """
        Retorna reservas do usuário autenticado, com filtro opcional por status.
        Exemplo de uso: /minhas-reservas?status=confirmada
        """
        user = request.user
        status_param = request.query_params.get("status", None)

        queryset = Reservation.objects.filter(user=user)

        if status_param:
            queryset = queryset.filter(status=status_param)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Save the user as the current user when creating a reservation.
        """
        serializer.save(user=self.request.user)
