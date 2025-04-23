from django.db import models
import uuid
from accounts.models import AdminUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Tabelog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    location_priority = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.5,
        verbose_name="現在地からの距離のの重要度",
    )
    price_priority = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.5,
        verbose_name="価格の重要度",
    )
    store_rating_priority = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.5,
        verbose_name="お店の評価の重要度",
    )
    decision_power_priority = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.5,
        verbose_name="決定権の重要度の反映度合いの重要度",
    )
    admin_user = models.OneToOneField(
        AdminUser, on_delete=models.CASCADE, related_name="tabelog"
    )

    def __str__(self):
        return str(self.admin_user.name) + "の食べログ設定"


class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=300, verbose_name="お店のURL", unique=True)
    name = models.CharField(max_length=100, verbose_name="お店の名前")
    lunch_price = models.IntegerField(
        null=True, blank=True, verbose_name="昼食の平均価格", default=0
    )
    dinner_price = models.IntegerField(
        null=True, blank=True, verbose_name="夕食の平均価格", default=0
    )
    walk_time_minutes = models.IntegerField(verbose_name="現在地からの徒歩時間（分）")
    genre = models.CharField(max_length=100, verbose_name="ジャンル")
    store_rating = models.FloatField(
        null=True, blank=True, verbose_name="お店の評価", default=0.0
    )
    final_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name="最終点数",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    tabelog = models.ForeignKey(Tabelog, on_delete=models.CASCADE, related_name="shops")

    def __str__(self):
        return self.name
