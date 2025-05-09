# Generated by Django 4.1.7 on 2024-08-12 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default="+205555555555",
                        max_length=30,
                        region=None,
                        verbose_name="phone number",
                    ),
                ),
                (
                    "about_me",
                    models.TextField(
                        default="Say something about yourself...",
                        verbose_name="about me",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")],
                        default="M",
                        max_length=20,
                        verbose_name="gender",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="EG", max_length=2, verbose_name="country"
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        default="Cairo", max_length=180, verbose_name="city"
                    ),
                ),
                (
                    "profile_photo",
                    models.ImageField(
                        default="/profile_default.png",
                        upload_to="",
                        verbose_name="profile photo",
                    ),
                ),
                (
                    "twitter_handle",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="twitter handle"
                    ),
                ),
                (
                    "followers",
                    models.ManyToManyField(
                        blank=True, related_name="following", to="profiles.profile"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
    ]
