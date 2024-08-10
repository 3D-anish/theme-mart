# Generated by Django 5.0.6 on 2024-07-16 05:47

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0015_alter_asset_category_required_file_types'),
        ('license', '0006_alter_asset_license_asset_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('canceled', 'Canceled')], default='pending', max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='order_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_asset_downloaded', models.BooleanField(default=False)),
                ('is_license_downloaded', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.asset')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='license.asset_license')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders')),
            ],
        ),
    ]
