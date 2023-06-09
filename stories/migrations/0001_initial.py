# Generated by Django 4.2 on 2023-05-27 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stories.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Stories",
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
                ("video", models.FileField(upload_to=stories.models.stories_location)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "viewers",
                    models.ManyToManyField(
                        blank=True, related_name="viewers", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
