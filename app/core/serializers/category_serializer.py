from rest_framework import serializers
from core.models import Category


class CategorySerializer(serializers.ModelSerializer):
    
    is_active = serializers.BooleanField(default=True, required=False)
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "image",
            "is_active",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "description": {"required": False},
        }

    def validate_name(self, value):
        if (
            Category.objects.exclude(pk=self.instance.pk if self.instance else None)
            .filter(name__iexact=value)
            .exists()
        ):
            raise serializers.ValidationError(
                "Esse nome de categoria já existe."
            )
        return value
