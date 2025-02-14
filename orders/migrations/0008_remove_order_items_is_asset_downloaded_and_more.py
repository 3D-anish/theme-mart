# Generated by Django 5.0.6 on 2024-07-18 08:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_orders_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_items',
            name='is_asset_downloaded',
        ),
        migrations.RemoveField(
            model_name='order_items',
            name='is_license_downloaded',
        ),
        migrations.AddField(
            model_name='orders',
            name='address_area',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='orders',
            name='address_city',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='orders',
            name='address_line_1',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='orders',
            name='address_line_2',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='orders',
            name='address_pincode',
            field=models.CharField(default='000000', max_length=6),
        ),
        migrations.AddField(
            model_name='orders',
            name='address_state',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='orders',
            name='gst_number',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='payment_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='orders',
            name='total_payment_recieved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='orders',
            name='user_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='orders',
            name='user_full_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='orders',
            name='user_phonenumber',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
