from rest_framework.viewsets import ModelViewSet
from core.serializers import CategorySerializer
from core.models import Category
from core.permissions import IsCategoryAdmin

from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsCategoryAdmin]


    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get("is_active")

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset
