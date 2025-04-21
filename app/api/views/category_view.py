from rest_framework.viewsets import ModelViewSet
from core.serializers import CategorySerializer
from core.models import Category
from core.permissions import IsCategoryAdmin

from rest_framework.permissions import IsAuthenticated


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsCategoryAdmin]
