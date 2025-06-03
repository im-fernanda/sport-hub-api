from rest_framework import serializers
from core.models import Space


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = [
            "id",
            "name",
            "description",
            "capacity",
            "category",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        name = data.get("name")
        category = data.get("category")
        instance = self.instance

        qs = Space.objects.filter(name__iexact=name, category=category)
        if instance:
            qs = qs.exclude(pk=instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                {"name": "Já existe um espaço com esse nome nesta categoria."}
            )

        return data
