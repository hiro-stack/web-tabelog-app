# Generated by Django 4.2.20 on 2025-04-23 06:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tabelog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('location_priority', models.FloatField(blank=True, default=0.5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='現在地からの距離のの重要度')),
                ('price_priority', models.FloatField(blank=True, default=0.5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='価格の重要度')),
                ('store_rating_priority', models.FloatField(blank=True, default=0.5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='お店の評価の重要度')),
                ('decision_power_priority', models.FloatField(blank=True, default=0.5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='決定権の重要度の反映度合いの重要度')),
                ('admin_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tabelog', to='accounts.adminuser')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=300, unique=True, verbose_name='お店のURL')),
                ('name', models.CharField(max_length=100, verbose_name='お店の名前')),
                ('lunch_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='昼食の平均価格')),
                ('dinner_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='夕食の平均価格')),
                ('walk_time_minutes', models.IntegerField(verbose_name='現在地からの徒歩時間（分）')),
                ('genre', models.CharField(max_length=100, verbose_name='ジャンル')),
                ('store_rating', models.FloatField(blank=True, default=0.0, null=True, verbose_name='お店の評価')),
                ('final_score', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='最終点数')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('tabelog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shops', to='tabelog.tabelog')),
            ],
        ),
    ]
