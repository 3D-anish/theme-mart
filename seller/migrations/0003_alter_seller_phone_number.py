# Generated by Django 5.0.6 on 2024-07-23 09:58

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_seller_bank_account_ifsc_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone Number'),
        ),
    ]