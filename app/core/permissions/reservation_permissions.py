from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReservationSelf(BasePermission):
    """
    Custom permission to only allow users to view or edit their own reservations.
    """

    def has_object_permission(self, request, view, obj):
        # Permite tudo se o usuário for admin
        if request.user.is_admin:
            return True

        # Permite deletar apenas se for o próprio requisitante
        if request.method == "DELETE":
            return obj.user == request.user

        # Para outras ações, permite se for admin ou o requisitante
        return obj.user == request.user
