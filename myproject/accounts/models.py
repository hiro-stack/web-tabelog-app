from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class AdminUser(models.Model):

    LUNCH_OR_DINNER_CHOICES = [
        ("dinner", "夕食"),
        ("lunch", "昼食"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    lunch_or_dinner = models.CharField(
        max_length=20,
        choices=LUNCH_OR_DINNER_CHOICES,
        default="lunch",
        verbose_name="Lunch or Dinner",
    )
    now_latitude = models.FloatField(null=True, blank=True)
    now_longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.name


class NormalUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    select_food = models.CharField(max_length=100, blank=True, null=True)
    ratio = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.5,
    )

    admin_user = models.ForeignKey(
        AdminUser, on_delete=models.CASCADE, related_name="normal_users"
    )

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=100)
    admin_user = models.ForeignKey(
        "AdminUser", on_delete=models.CASCADE, related_name="stations"
    )

    def __str__(self):
        return self.name
