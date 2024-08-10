# Generated by Django 5.0.6 on 2024-07-27 11:25

import seller.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_alter_seller_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='aadhar_card_number',
            field=models.CharField(default='123', max_length=50, validators=[seller.validators.aadhar_card_number_validator], verbose_name=' Aadhar Card Number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seller',
            name='bank_account_ifsc_code',
            field=models.CharField(max_length=100, validators=[seller.validators.account_ifsc_code_validator], verbose_name='Bank Account IFSC Code'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='bank_account_number',
            field=models.CharField(max_length=100, validators=[seller.validators.account_number_validator], verbose_name='Bank Account Number'),
        ),
    ]
