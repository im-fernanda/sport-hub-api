# Generated by Django 5.2 on 2025-05-15 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_alter_reservation_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(upload_to=""),
        ),
    ]
