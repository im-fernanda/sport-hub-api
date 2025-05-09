from rest_framework.viewsets import ModelViewSet
from core.serializers import UserSerializer
from core.models import User
from core.permissions import IsAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(detail=False, methods=["get"])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get("is_active")
        is_admin = self.request.query_params.get("is_admin")

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        if is_admin is not None:
            queryset = queryset.filter(is_admin=is_admin.lower() == "true")

        return queryset

    def get_permissions(self):
        if self.action == "me":
            return [IsAuthenticated()]

        return super().get_permissions()
    

    