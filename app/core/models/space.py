from django.db import models


class Space(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField()
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="spaces"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
