from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=255, unique=False)  # Deixe o unique=False aqui
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="")
    is_active = models.BooleanField(default=True)

    def clean(self):
        # Normaliza para minúsculo e busca duplicadas (case-insensitive)
        if Category.objects.exclude(pk=self.pk).filter(name__iexact=self.name).exists():
            raise ValidationError(
                {"name": "Já existe uma categoria com esse nome (case-insensitive)."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Chama o clean() automaticamente antes de salvar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
