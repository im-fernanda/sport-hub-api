from django.core.exceptions import ValidationError
from django.db import models


class Space(models.Model):
    name = models.CharField(max_length=255, unique=False)  # Tiramos o unique=True
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField()
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="spaces"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        # Verifica se já existe um espaço com o mesmo nome (case-insensitive) na mesma categoria
        existing = Space.objects.exclude(pk=self.pk).filter(
            category=self.category, name__iexact=self.name
        )
        if existing.exists():
            raise ValidationError(
                {"name": "Já existe um espaço com esse nome nesta categoria."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
