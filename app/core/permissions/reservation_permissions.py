from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReservationSelf(BasePermission):
    """
    Custom permission to only allow users to view or edit their own reservations.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE" and not request.user.is_admin:
            return False
        return request.user.is_admin or obj.user == request.user
