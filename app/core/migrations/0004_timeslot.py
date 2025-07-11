# Generated by Django 5.2 on 2025-04-20 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("is_holiday", models.BooleanField(blank=True, default=False)),
            ],
        ),
    ]
