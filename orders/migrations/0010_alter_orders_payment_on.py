# Generated by Django 5.0.6 on 2024-07-19 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_orders_other_razorpay_payment_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='payment_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
