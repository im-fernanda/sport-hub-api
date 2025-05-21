from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Custom permission to only allow admins to access certain views.
    """

    def has_permission(self, request, view):
        if request.method in ("POST", "GET", "DELETE"):
            return request.user.is_admin

        return True

    def has_object_permission(self, request, view, obj):
        if (
            request.method in ("PATCH", "PUT")
            and request.data.get("is_admin") is not None
            or request.data.get("is_active") is not None
            or request.data.get("is_first_login") is not None
        ):
            return request.user.is_admin

        return True
